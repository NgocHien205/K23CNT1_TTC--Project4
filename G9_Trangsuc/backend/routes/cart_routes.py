# ==============================
# FILE: routes/cart_routes.py
# CHỨC NĂNG:
# - Xem giỏ hàng
# - Thêm sản phẩm vào giỏ
# - Cập nhật số lượng
# - Xóa sản phẩm khỏi giỏ
# ==============================

from flask import Blueprint, jsonify, request
from database.db import get_connection, rows_to_dict

cart_bp = Blueprint("cart", __name__)


# ==============================
# API LẤY GIỎ HÀNG THEO USER
# URL: /api/cart/<user_id>
# ==============================
@cart_bp.route("/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            ct.G9_MaChiTiet AS cart_detail_id,
            gh.G9_MaGioHang AS cart_id,
            sp.G9_MaSanPham AS product_id,
            sp.G9_TenSanPham AS product_name,
            sp.G9_HinhAnhChinh AS image,
            ct.G9_SoLuong AS quantity,
            ct.G9_DonGia AS price,
            ct.G9_SoLuong * ct.G9_DonGia AS total
        FROM G9_GioHang gh
        INNER JOIN G9_ChiTietGioHang ct
            ON gh.G9_MaGioHang = ct.G9_MaGioHang
        INNER JOIN G9_SanPham sp
            ON ct.G9_MaSanPham = sp.G9_MaSanPham
        WHERE gh.G9_MaNguoiDung = ?
    """, (user_id,))

    data = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy giỏ hàng thành công",
        "data": data
    })


# ==============================
# API THÊM SẢN PHẨM VÀO GIỎ
# BODY: user_id, product_id, quantity
# ==============================
@cart_bp.route("/add", methods=["POST"])
def add_to_cart():
    data = request.json

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    conn = get_connection()
    cursor = conn.cursor()

    # Lấy giá sản phẩm
    cursor.execute("""
        SELECT G9_Gia 
        FROM G9_SanPham 
        WHERE G9_MaSanPham = ?
    """, (product_id,))
    product = cursor.fetchone()

    if not product:
        cursor.close()
        conn.close()
        return jsonify({
            "success": False,
            "message": "Sản phẩm không tồn tại"
        }), 404

    price = product[0]

    # Kiểm tra user đã có giỏ hàng chưa
    cursor.execute("""
        SELECT G9_MaGioHang 
        FROM G9_GioHang 
        WHERE G9_MaNguoiDung = ?
    """, (user_id,))
    cart = cursor.fetchone()

    # Nếu chưa có giỏ hàng thì tạo mới
    if not cart:
        cursor.execute("""
            INSERT INTO G9_GioHang(G9_MaNguoiDung)
            OUTPUT INSERTED.G9_MaGioHang
            VALUES(?)
        """, (user_id,))
        cart_id = cursor.fetchone()[0]
    else:
        cart_id = cart[0]

    # Kiểm tra sản phẩm đã có trong giỏ chưa
    cursor.execute("""
        SELECT G9_MaChiTiet, G9_SoLuong
        FROM G9_ChiTietGioHang
        WHERE G9_MaGioHang = ? AND G9_MaSanPham = ?
    """, (cart_id, product_id))
    item = cursor.fetchone()

    if item:
        # Nếu có rồi thì cộng thêm số lượng
        cursor.execute("""
            UPDATE G9_ChiTietGioHang
            SET G9_SoLuong = G9_SoLuong + ?
            WHERE G9_MaChiTiet = ?
        """, (quantity, item[0]))
    else:
        # Nếu chưa có thì thêm mới
        cursor.execute("""
            INSERT INTO G9_ChiTietGioHang
            (G9_MaGioHang, G9_MaSanPham, G9_SoLuong, G9_DonGia)
            VALUES (?, ?, ?, ?)
        """, (cart_id, product_id, quantity, price))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Thêm vào giỏ hàng thành công"
    })


# ==============================
# API CẬP NHẬT SỐ LƯỢNG
# BODY: quantity
# ==============================
@cart_bp.route("/update/<int:cart_detail_id>", methods=["PUT"])
def update_cart(cart_detail_id):
    data = request.json
    quantity = int(data.get("quantity", 1))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_ChiTietGioHang
        SET G9_SoLuong = ?
        WHERE G9_MaChiTiet = ?
    """, (quantity, cart_detail_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật giỏ hàng thành công"
    })


# ==============================
# API XÓA SẢN PHẨM KHỎI GIỎ
# ==============================
@cart_bp.route("/delete/<int:cart_detail_id>", methods=["DELETE"])
def delete_cart_item(cart_detail_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM G9_ChiTietGioHang
        WHERE G9_MaChiTiet = ?
    """, (cart_detail_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Xóa sản phẩm khỏi giỏ hàng thành công"
    })