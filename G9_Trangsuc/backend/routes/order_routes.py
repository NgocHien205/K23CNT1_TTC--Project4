from flask import Blueprint, jsonify, request

order_bp = Blueprint("orders", __name__)

orders = []

@order_bp.route("/", methods=["GET"])
def get_orders():
    return jsonify({
        "success": True,
        "message": "Lấy danh sách đơn hàng thành công",
        "data": orders
    })

@order_bp.route("/", methods=["POST"])
def create_order():
    data = request.json

    new_order = {
        "id": len(orders) + 1,
        "customer_name": data.get("customer_name"),
        "phone": data.get("phone"),
        "address": data.get("address"),
        "total": data.get("total"),
        "status": "Chờ xác nhận"
    }

    orders.append(new_order)

    return jsonify({
        "success": True,
        "message": "Đặt hàng thành công",
        "data": new_order
    })