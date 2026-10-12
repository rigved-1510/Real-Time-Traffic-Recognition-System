# NITK TrafficVision — Real-Time Indian Traffic Sign Recognition System

A full-stack, enterprise-grade web application and backend recognition pipeline built for detecting, classifying, and explaining Indian traffic signs in real time from live camera feeds or uploaded videos.

Developed according to the Software Requirements Specification (SRS), Data Flow Diagram (DFD), and Structure Chart for IT303.

---

## 🚀 Key Features

### 1. Robust Security & Authentication
- **User Authentication:** Bcrypt password hashing, session tokens, brute-force lockout (account locked after 5 failed attempts for 15 minutes).
- **Two-Factor Authentication (2FA):** Standard TOTP (Google Authenticator, Microsoft Authenticator) with QR code setup, one-time backup codes, and OTP validation.
- **Server-Side Session Management:** Active login sessions stored in MySQL, allowing immediate remote session revocation from user profile or admin console.
- **Activity Audit Trail:** Comprehensive event logging (`login_success`, `login_failure`, `account_locked`, `otp_verify`, `register`, `admin_action`, `password_change`, `logout`) with IP addresses and metadata.

### 2. Live Recognition & Video Processing
- **Webcam Real-Time Detection:** Live webcam capture using HTML5 `getUserMedia`, frame transmission, dynamic canvas bounding box rendering, and real-time FPS badge.
- **Video File Upload:** Drag-and-drop upload supporting MP4, AVI, MOV, WEBM (up to 100MB) with simulated progress indicators and detection results aggregation.
- **Detection Result Breakdown:** Bounding boxes, confidence score bars, category tagging (Mandatory, Cautionary, Informatory), and legal meanings.

### 3. Traffic Sign Meaning Dictionary
- Catalog of Indian traffic sign classes based on IRC standards.
- Searchable by sign name, class ID, or legal description.
- Filterable by Category: **Mandatory** (Red), **Cautionary** (Amber), and **Informatory** (Cyan).

### 4. Administrator Console
- **System Overview:** Total registered users, active sessions, total detections, sign dictionary count, and top recognized signs.
- **User Management:** View all users, toggle roles (`user` ↔ `admin`), unlock brute-force locked accounts, revoke sessions, and delete accounts.
- **Activity Audit Logs:** Filterable by event type, user ID, date range, pagination, and raw JSON metadata inspector.

### 5. ML Pipeline Integration (Teammate Model Ready)
- The pipeline in `Backend/ml/pipeline.py` is configured to load:
  - `ml/weights/yolo_best.pt` (Ultralytics YOLO for sign localization)
  - `ml/weights/cnn_best.pth` (PyTorch CNN for fine-grained Indian traffic sign classification)
- **Automatic Fallback:** When model weights are not yet present while your teammate trains the model, the backend runs in realistic **STUB MODE** returning plausible bounding boxes and classifications so UI and API workflows function out-of-the-box.

---

## 🛠️ Technology Stack

- **Frontend:** Pure HTML5, Modern Vanilla CSS3 (Custom Properties design system, dark-mode glassmorphism, responsive grid), Vanilla JavaScript (ES Modules).
- **Backend:** Python 3.9+, Flask REST API, Flask-CORS, PyOTP, QRcode, MySQL Connector.
- **Database:** MySQL 8.0+ with foreign key constraints, indexes, and automated triggers.

---

## 📁 Project Structure

```
Code/
├── Backend/
│   ├── app.py                      # Flask application factory and blueprints
│   ├── config.py                   # Environment configuration loader
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Template configuration file
│   ├── db/
│   │   ├── connection.py           # MySQL connection pool
│   │   ├── users.py                # User queries & password management
│   │   ├── sessions_db.py          # Server-side session tokens & revocation
│   │   ├── activity_logs.py        # Security audit log queries
│   │   ├── detection.py            # Recognition session & detection storage
│   │   └── signs.py                # Sign meaning dictionary queries
│   ├── middleware/
│   │   └── auth_middleware.py      # @require_auth & @require_admin decorators
│   ├── routes/
│   │   ├── auth.py                 # Sign-in, sign-up, 2FA, OTP endpoints
│   │   ├── user.py                 # Profile, password, sessions endpoints
│   │   ├── admin.py                # Admin metrics, user CRUD, audit logs
│   │   ├── detection.py            # Stream frame, upload video, session history
│   │   └── signs.py                # Sign dictionary endpoints
│   └── ml/
│       ├── pipeline.py             # ML loader & detection pipeline (with stub mode)
│       └── weights/                # Directory for teammate's trained weights
├── Database/
│   ├── schema.sql                  # Complete MySQL schema (tables, indexes, triggers)
│   └── seed.sql                    # Seed data (Indian traffic signs dictionary & admin user)
├── Frontend/
│   ├── index.html                  # Sign-in page
│   ├── register.html               # Registration page with strength meter
│   ├── verify-otp.html             # 2FA 6-digit OTP verification
│   ├── setup-2fa.html              # TOTP QR code & backup codes setup
│   ├── dashboard.html              # Main dashboard: live camera & video upload
│   ├── history.html                # Past sessions and detection drill-down
│   ├── profile.html                # User profile, password change & active sessions
│   ├── signs.html                  # Sign meaning dictionary browser
│   ├── admin/
│   │   ├── index.html              # Admin KPI overview & analytics
│   │   ├── users.html              # User management & account unlock
│   │   ├── logs.html               # Activity audit logs viewer
│   │   └── signs.html              # Sign dictionary admin view
│   ├── css/
│   │   └── style.css               # Complete design system & responsive styling
│   └── js/
│       ├── utils.js                # Auth storage, toasts, formatters
│       ├── api.js                  # Centralized REST API client
│       ├── auth.js                 # Auth helper workflows
│       ├── dashboard.js            # Live camera controller & canvas overlays
│       ├── upload.js               # Video drag-and-drop upload handler
│       ├── admin.js                # Admin operations
│       ├── history.js              # History fetching
│       ├── profile.js              # Profile operations
│       └── signs.js                # Sign catalog helpers
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Database Setup
Ensure you have MySQL 8.0+ running. Open your MySQL client (e.g., MySQL Workbench or MySQL CLI) and execute:
```bash
mysql -u root -p < Database/schema.sql
mysql -u root -p traffic_sign_db < Database/seed.sql
```

### 2. Backend Setup
1. Open a terminal in `Backend/`:
   ```bash
   cd Backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   Copy `.env.example` to `.env` and adjust your MySQL password:
   ```bash
   cp .env.example .env
   ```
5. Start the backend server:
   ```bash
   python app.py
   ```
   The Flask API will run at `http://localhost:5000`.

### 3. Frontend Setup
You can serve the `Frontend` folder using any static HTTP server (such as VSCode Live Server, Python's built-in HTTP server, or Nginx):
```bash
cd Frontend
python -m http.server 5500
```
Open your browser and navigate to:
`http://localhost:5500/index.html`

### 4. Default Seed Administrator Account
- **Username:** `admin`
- **Email:** `admin@trafficvision.local`
- **Password:** `Admin@12345` (set in `Database/seed.sql`)

---

## 🧠 Connecting Your Teammate's Trained Model
When your teammate completes training:
1. Place the trained YOLO weights at `Backend/ml/weights/yolo_best.pt`.
2. Place the CNN classifier weights at `Backend/ml/weights/cnn_best.pth`.
3. Restart the Flask app (`python app.py`).
4. The system automatically detects the weights, transitions out of **STUB MODE**, and executes live PyTorch / YOLO inferences!
