from flask import Blueprint, jsonify

gold_bp = Blueprint("gold", __name__)

@gold_bp.route("/", methods=["GET"])
def get_gold_price():
    return jsonify({
        "success": True,
        "message": "Lấy giá vàng thành công",
        "data": {
            "gold_9999_buy": 85000000,
            "gold_9999_sell": 87000000,
            "unit": "VNĐ/lượng"
        }
    })