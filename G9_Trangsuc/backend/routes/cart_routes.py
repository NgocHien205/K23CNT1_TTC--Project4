from flask import Blueprint, jsonify, request

cart_bp = Blueprint("cart", __name__)

cart_items = []

@cart_bp.route("/", methods=["GET"])
def get_cart():
    return jsonify({
        "success": True,
        "message": "Lấy giỏ hàng thành công",
        "data": cart_items
    })

@cart_bp.route("/add", methods=["POST"])
def add_to_cart():
    data = request.json
    cart_items.append(data)

    return jsonify({
        "success": True,
        "message": "Thêm vào giỏ hàng thành công",
        "data": data
    })

@cart_bp.route("/clear", methods=["DELETE"])
def clear_cart():
    cart_items.clear()

    return jsonify({
        "success": True,
        "message": "Đã xóa giỏ hàng"
    })