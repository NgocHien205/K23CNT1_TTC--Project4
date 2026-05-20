from flask import Blueprint, jsonify

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/", methods=["GET"])
def admin_home():
    return jsonify({
        "success": True,
        "message": "Khu vực quản trị admin"
    })