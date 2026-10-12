"""
ml/pipeline.py — Traffic sign recognition pipeline.

Single-stage YOLO inference using best.pt.
The model detects AND classifies traffic signs in one forward pass —
no separate CNN stage required.

Falls back to a realistic stub when the weight file is not found, so
the UI and API work even during development.
"""
import base64
import logging
import random
import time
from pathlib import Path

import cv2
import numpy as np

from config import Config

logger = logging.getLogger(__name__)

# ── Module-level state (loaded once at startup) ──────────────────────────────
_yolo_model = None
_sign_labels: list[dict] = []   # rows from sign_meaning_dictionary table
_yolo_class_names: dict[int, str] = {}  # {0: '200 meters', 1: '50 to 100 meters', ...}

WEIGHTS_READY = False


# ── Class name → DB sign mapping ─────────────────────────────────────────────
# Maps YOLO class names (from best.pt) to sign_meaning_dictionary categories
# and meanings so detections show rich descriptions in the UI.
_YOLO_CLASS_META: dict[str, dict] = {
    "200 meters":             {"category": "informatory",  "meaning": "Distance marker: 200 metres ahead."},
    "50 to 100 meters":       {"category": "informatory",  "meaning": "Distance marker: 50 to 100 metres ahead."},
    "Cross Road":             {"category": "cautionary",   "meaning": "Cross road intersection ahead; slow down and watch for cross traffic."},
    "Gap in Median":          {"category": "cautionary",   "meaning": "Opening in the road median; beware of vehicles crossing or turning."},
    "Hump":                   {"category": "cautionary",   "meaning": "Speed breaker / road hump ahead; reduce speed."},
    "Lefthand Curve":         {"category": "cautionary",   "meaning": "Dangerous left-hand curve ahead; reduce speed accordingly."},
    "MajorRoad Ahead":        {"category": "cautionary",   "meaning": "Major road intersection ahead; yield to traffic on the main road."},
    "Men at Work":            {"category": "cautionary",   "meaning": "Road works / construction crew ahead; proceed with caution."},
    "Narrow Bridge":          {"category": "cautionary",   "meaning": "Narrow bridge or carriageway ahead; reduce speed and watch for oncoming vehicles."},
    "Pedestrain":             {"category": "cautionary",   "meaning": "Pedestrian crossing ahead; give way to pedestrians."},
    "RightHandCurve":         {"category": "cautionary",   "meaning": "Dangerous right-hand curve ahead; reduce speed accordingly."},
    "School Ahead":           {"category": "cautionary",   "meaning": "School zone ahead; children may cross — drive slowly."},
    "SideRoadLeft":           {"category": "cautionary",   "meaning": "Side road joining from the left ahead; watch for merging vehicles."},
    "SideRoadRight":          {"category": "cautionary",   "meaning": "Side road joining from the right ahead; watch for merging vehicles."},
    "Slippery Road":          {"category": "cautionary",   "meaning": "Slippery road surface ahead; reduce speed and avoid sudden braking."},
    "Staggered Intersection": {"category": "cautionary",   "meaning": "Staggered or offset intersection ahead; approach with care."},
    "Y-Intersection":         {"category": "cautionary",   "meaning": "Y-shaped road intersection ahead; yield appropriately."},
}


def load_models():
    """Called once at application startup. Loads YOLO model if weight file exists."""
    global _yolo_model, _sign_labels, _yolo_class_names, WEIGHTS_READY

    # Load sign dictionary from DB for rich descriptions
    try:
        from db.signs import get_all_signs
        _sign_labels = get_all_signs(limit=500)
        logger.info(f"Loaded {len(_sign_labels)} sign labels from DB")
    except Exception as e:
        logger.warning(f"Could not load sign labels from DB: {e}")
        _sign_labels = []

    yolo_path = Path(Config.YOLO_WEIGHTS)

    if yolo_path.exists():
        try:
            from ultralytics import YOLO
            _yolo_model = YOLO(str(yolo_path))
            _yolo_class_names = _yolo_model.names  # {int: str}
            WEIGHTS_READY = True
            logger.info(
                f"YOLO model loaded from {yolo_path} — "
                f"{len(_yolo_class_names)} classes: {list(_yolo_class_names.values())}"
            )
            logger.info("ML pipeline ready — REAL inference mode ✓")
        except Exception as e:
            logger.error(f"YOLO model load failed: {e}")
            WEIGHTS_READY = False
    else:
        logger.warning(
            f"Weight file not found at '{yolo_path}'. Running in STUB mode. "
            "Place best.pt in Backend/ml/weights/ to enable real inference."
        )
        WEIGHTS_READY = False


def process_frame(frame_b64: str) -> dict:
    """
    Process a single base64-encoded JPEG/PNG frame through the YOLO model.

    Returns:
        {
          "detections": [
              {
                "class_id":    int,
                "sign_name":   str,
                "sign_meaning": str,
                "category":    str,
                "confidence":  float,       # 0.0 – 1.0
                "bbox":        [x, y, w, h] # normalised 0–1
              }, ...
          ],
          "fps":             float,
          "annotated_frame": str,   # base64 JPEG with bounding boxes
          "mode":            "real" | "stub"
        }
    """
    t_start = time.perf_counter()

    # ── Decode incoming frame ────────────────────────────────────────────────
    try:
        img_bytes = base64.b64decode(frame_b64)
        arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("cv2.imdecode returned None — not a valid image")
    except Exception as e:
        return {"error": f"Frame decode failed: {e}", "detections": [], "fps": 0, "mode": "error"}

    # ── Run inference ────────────────────────────────────────────────────────
    if WEIGHTS_READY:
        detections = _yolo_inference(frame)
        mode = "real"
    else:
        detections = _stub_inference(frame)
        mode = "stub"

    # ── Draw overlays and encode back to base64 ──────────────────────────────
    annotated = _draw_overlays(frame.copy(), detections)
    _, buf = cv2.imencode(".jpg", annotated, [cv2.IMWRITE_JPEG_QUALITY, 85])
    annotated_b64 = base64.b64encode(buf).decode()

    elapsed = time.perf_counter() - t_start
    fps = round(1.0 / elapsed, 1) if elapsed > 0 else 0.0

    return {
        "detections":      detections,
        "fps":             fps,
        "annotated_frame": annotated_b64,
        "mode":            mode,
    }


# ── Real YOLO inference ───────────────────────────────────────────────────────

def _yolo_inference(frame: np.ndarray) -> list[dict]:
    """Run best.pt YOLO detection. YOLO outputs class_id + confidence directly."""
    h, w = frame.shape[:2]
    results = _yolo_model.predict(frame, verbose=False, conf=Config.CONF_THRESHOLD)
    detections = []

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = round(float(box.conf[0]), 3)
        class_id   = int(box.cls[0])
        class_name = _yolo_class_names.get(class_id, f"Class {class_id}")

        # Look up rich metadata
        meta = _YOLO_CLASS_META.get(class_name, {})
        category = meta.get("category", "cautionary")
        meaning  = meta.get("meaning", class_name)

        detections.append({
            "class_id":    class_id,
            "sign_name":   class_name,
            "sign_meaning": meaning,
            "category":    category,
            "confidence":  confidence,
            "bbox": [
                round(x1 / w, 4),
                round(y1 / h, 4),
                round((x2 - x1) / w, 4),
                round((y2 - y1) / h, 4),
            ],
        })

    return detections


# ── Stub inference (no model) ─────────────────────────────────────────────────

def _stub_inference(frame: np.ndarray) -> list[dict]:
    """Return 0–2 plausible random detections from known YOLO classes for UI dev."""
    class_pool = list(_YOLO_CLASS_META.items()) if _YOLO_CLASS_META else []
    if not class_pool:
        return []

    n = random.choices([0, 1, 2], weights=[0.3, 0.5, 0.2])[0]
    detections = []
    for i in range(n):
        name, meta = random.choice(class_pool)
        detections.append({
            "class_id":    i,
            "sign_name":   name,
            "sign_meaning": meta.get("meaning", name),
            "category":    meta.get("category", "cautionary"),
            "confidence":  round(random.uniform(0.50, 0.97), 3),
            "bbox": [
                round(random.uniform(0.05, 0.50), 3),
                round(random.uniform(0.05, 0.50), 3),
                round(random.uniform(0.15, 0.30), 3),
                round(random.uniform(0.15, 0.30), 3),
            ],
        })
    return detections


# ── Bounding box drawing ──────────────────────────────────────────────────────

def _draw_overlays(frame: np.ndarray, detections: list[dict]) -> np.ndarray:
    h, w = frame.shape[:2]
    for d in detections:
        bx, by, bw, bh = d["bbox"]
        x1 = int(bx * w);       y1 = int(by * h)
        x2 = int((bx + bw) * w); y2 = int((by + bh) * h)

        # Colour by category
        cat = d.get("category", "cautionary")
        if cat == "mandatory":
            color = (80, 80, 230)    # red-ish
        elif cat == "informatory":
            color = (230, 180, 30)   # blue
        else:
            color = (30, 220, 180)   # cyan (cautionary default)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        label = f"{d['sign_name']}  {d['confidence'] * 100:.0f}%"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.52, 1)
        cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)
        cv2.putText(frame, label, (x1 + 3, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.52, (0, 0, 0), 1, cv2.LINE_AA)
    return frame
