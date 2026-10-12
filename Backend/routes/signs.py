"""routes/signs.py — Sign dictionary endpoints."""
from flask import Blueprint, request, jsonify
from db.signs import get_all_signs, get_sign_by_id, search_signs, get_signs_by_category, count_signs
from middleware.auth_middleware import require_auth

signs_bp = Blueprint("signs", __name__, url_prefix="/api/signs")


@signs_bp.route("", methods=["GET"])
@require_auth
def list_signs():
    limit    = int(request.args.get("limit",  100))
    offset   = int(request.args.get("offset", 0))
    category = request.args.get("category")

    if category:
        signs = get_signs_by_category(category)
    else:
        signs = get_all_signs(limit, offset)

    return jsonify({"signs": signs, "total": count_signs()}), 200


@signs_bp.route("/search", methods=["GET"])
@require_auth
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "q parameter required"}), 400
    return jsonify({"signs": search_signs(q)}), 200


@signs_bp.route("/<int:class_id>", methods=["GET"])
@require_auth
def get_sign(class_id: int):
    sign = get_sign_by_id(class_id)
    if not sign:
        return jsonify({"error": "Sign not found"}), 404
    return jsonify(sign), 200
