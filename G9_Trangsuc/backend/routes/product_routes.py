from flask import Blueprint, jsonify, request

# ==============================
# TẠO BLUEPRINT PRODUCT
# ==============================
product_bp = Blueprint("products", __name__)

# ==============================
# DỮ LIỆU SẢN PHẨM MẪU
# ==============================
products = [
    {
        "id": 1,
        "name": "Nhẫn vàng 18K",
        "price": 5000000,
        "image": "ring.jpg"
    },
    {
        "id": 2,
        "name": "Dây chuyền bạc",
        "price": 1200000,
        "image": "necklace.jpg"
    }
]

# ==============================
# LẤY DANH SÁCH SẢN PHẨM
# ==============================
@product_bp.route("/", methods=["GET"])
def get_products():
    return jsonify({
        "success": True,
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    })

# ==============================
# LẤY CHI TIẾT SẢN PHẨM
# ==============================
@product_bp.route("/<int:id>", methods=["GET"])
def get_product_detail(id):
    for product in products:
        if product["id"] == id:
            return jsonify({
                "success": True,
                "message": "Lấy chi tiết sản phẩm thành công",
                "data": product
            })

    return jsonify({
        "success": False,
        "message": "Không tìm thấy sản phẩm"
    }), 404

# ==============================
# THÊM SẢN PHẨM
# ==============================
@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.json

    new_product = {
        "id": len(products) + 1,
        "name": data.get("name"),
        "price": data.get("price"),
        "image": data.get("image")
    }

    products.append(new_product)

    return jsonify({
        "success": True,
        "message": "Thêm sản phẩm thành công",
        "data": new_product
    })