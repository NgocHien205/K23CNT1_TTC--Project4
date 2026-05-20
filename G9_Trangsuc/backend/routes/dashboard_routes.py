from flask import Blueprint, jsonify

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    return jsonify({
        "success": True,
        "message": "Thống kê dashboard",
        "data": {
            "total_products": 20,
            "total_orders": 15,
            "total_users": 8,
            "revenue": 120000000
        }
    })