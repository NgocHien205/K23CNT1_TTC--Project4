# ==============================
# FILE: routes/order_routes.py
# CHỨC NĂNG:
# - Xem đơn hàng
# - Tạo đơn hàng từ giỏ hàng
# - Xem chi tiết đơn hàng
# - Admin cập nhật trạng thái đơn hàng
# ==============================

from flask import Blueprint, jsonify, request
from database.db import get_connection, rows_to_dict, row_to_dict

order_bp = Blueprint("orders", __name__)


# ==============================
# API LẤY TẤT CẢ ĐƠN HÀNG
# URL: /api/orders/
# ==============================
@order_bp.route("/", methods=["GET"])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            dh.G9_MaDonHang AS id,
            nd.G9_HoTen AS customer_name,
            dh.G9_TenNguoiNhan AS receiver_name,
            dh.G9_SDTNhan AS phone,
            dh.G9_DiaChiGiao AS address,
            dh.G9_TongTien AS total,
            dh.G9_TrangThai AS status,
            dh.G9_NgayDat AS created_at
        FROM G9_DonHang dh
        INNER JOIN G9_NguoiDung nd
            ON dh.G9_MaNguoiDung = nd.G9_MaNguoiDung
        ORDER BY dh.G9_MaDonHang DESC
    """)

    data = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy danh sách đơn hàng thành công",
        "data": data
    })


# ==============================
# API LẤY ĐƠN HÀNG THEO USER
# URL: /api/orders/user/2
# ==============================
@order_bp.route("/user/<int:user_id>", methods=["GET"])
def get_orders_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            G9_MaDonHang AS id,
            G9_TenNguoiNhan AS receiver_name,
            G9_SDTNhan AS phone,
            G9_DiaChiGiao AS address,
            G9_TongTien AS total,
            G9_TrangThai AS status,
            G9_NgayDat AS created_at
        FROM G9_DonHang
        WHERE G9_MaNguoiDung = ?
        ORDER BY G9_MaDonHang DESC
    """, (user_id,))

    data = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy đơn hàng theo người dùng thành công",
        "data": data
    })


# ==============================
# API XEM CHI TIẾT ĐƠN HÀNG
# URL: /api/orders/detail/1
# ==============================
@order_bp.route("/detail/<int:order_id>", methods=["GET"])
def get_order_detail(order_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Lấy thông tin đơn hàng
    cursor.execute("""
        SELECT 
            G9_MaDonHang AS id,
            G9_TenNguoiNhan AS receiver_name,
            G9_SDTNhan AS phone,
            G9_DiaChiGiao AS address,
            G9_TongTien AS total,
            G9_TrangThai AS status,
            G9_NgayDat AS created_at
        FROM G9_DonHang
        WHERE G9_MaDonHang = ?
    """, (order_id,))

    order = row_to_dict(cursor)

    # Lấy danh sách sản phẩm trong đơn
    cursor.execute("""
        SELECT
            ct.G9_MaChiTiet AS id,
            sp.G9_TenSanPham AS product_name,
            sp.G9_HinhAnhChinh AS image,
            ct.G9_SoLuong AS quantity,
            ct.G9_DonGia AS price,
            ct.G9_ThanhTien AS total
        FROM G9_ChiTietDonHang ct
        INNER JOIN G9_SanPham sp
            ON ct.G9_MaSanPham = sp.G9_MaSanPham
        WHERE ct.G9_MaDonHang = ?
    """, (order_id,))

    items = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy chi tiết đơn hàng thành công",
        "data": {
            "order": order,
            "items": items
        }
    })


# ==============================
# API TẠO ĐƠN HÀNG TỪ GIỎ HÀNG
# BODY: user_id, receiver_name, phone, address, payment_method
# ==============================
@order_bp.route("/checkout", methods=["POST"])
def checkout():
    data = request.json

    user_id = data.get("user_id")
    receiver_name = data.get("receiver_name")
    phone = data.get("phone")
    address = data.get("address")
    payment_method = data.get("payment_method", "COD")

    conn = get_connection()
    cursor = conn.cursor()

    # Lấy giỏ hàng của user
    cursor.execute("""
        SELECT G9_MaGioHang
        FROM G9_GioHang
        WHERE G9_MaNguoiDung = ?
    """, (user_id,))

    cart = cursor.fetchone()

    if not cart:
        cursor.close()
        conn.close()
        return jsonify({
            "success": False,
            "message": "Giỏ hàng trống"
        }), 400

    cart_id = cart[0]

    # Lấy chi tiết giỏ hàng
    cursor.execute("""
        SELECT 
            G9_MaSanPham,
            G9_SoLuong,
            G9_DonGia,
            G9_SoLuong * G9_DonGia AS ThanhTien
        FROM G9_ChiTietGioHang
        WHERE G9_MaGioHang = ?
    """, (cart_id,))

    cart_items = cursor.fetchall()

    if not cart_items:
        cursor.close()
        conn.close()
        return jsonify({
            "success": False,
            "message": "Giỏ hàng chưa có sản phẩm"
        }), 400

    # Tính tổng tiền
    total = sum([item.ThanhTien for item in cart_items])

    # Tạo đơn hàng
    cursor.execute("""
        INSERT INTO G9_DonHang
        (
            G9_MaNguoiDung,
            G9_TenNguoiNhan,
            G9_SDTNhan,
            G9_DiaChiGiao,
            G9_TongTien
        )
        OUTPUT INSERTED.G9_MaDonHang
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, receiver_name, phone, address, total))

    order_id = cursor.fetchone()[0]

    # Thêm chi tiết đơn hàng
    for item in cart_items:
        cursor.execute("""
            INSERT INTO G9_ChiTietDonHang
            (
                G9_MaDonHang,
                G9_MaSanPham,
                G9_SoLuong,
                G9_DonGia
            )
            VALUES (?, ?, ?, ?)
        """, (order_id, item.G9_MaSanPham, item.G9_SoLuong, item.G9_DonGia))

        # Trừ tồn kho sản phẩm
        cursor.execute("""
            UPDATE G9_SanPham
            SET G9_SoLuongTon = G9_SoLuongTon - ?
            WHERE G9_MaSanPham = ?
        """, (item.G9_SoLuong, item.G9_MaSanPham))

    # Tạo bản ghi thanh toán
    cursor.execute("""
        INSERT INTO G9_ThanhToan
        (
            G9_MaDonHang,
            G9_PhuongThuc,
            G9_SoTien
        )
        VALUES (?, ?, ?)
    """, (order_id, payment_method, total))

    # Xóa chi tiết giỏ hàng sau khi đặt hàng
    cursor.execute("""
        DELETE FROM G9_ChiTietGioHang
        WHERE G9_MaGioHang = ?
    """, (cart_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Đặt hàng thành công",
        "order_id": order_id
    })


# ==============================
# API CẬP NHẬT TRẠNG THÁI ĐƠN HÀNG
# BODY: status
# ==============================
@order_bp.route("/status/<int:order_id>", methods=["PUT"])
def update_order_status(order_id):
    data = request.json
    status = data.get("status")

    conn = get_connection()
    cursor = conn.cursor()

    # Cập nhật trạng thái đơn hàng
    cursor.execute("""
        UPDATE G9_DonHang
        SET G9_TrangThai = ?
        WHERE G9_MaDonHang = ?
    """, (status, order_id))

    # Lưu lịch sử trạng thái
    cursor.execute("""
        INSERT INTO G9_LichSuTrangThaiDonHang
        (
            G9_MaDonHang,
            G9_TrangThai
        )
        VALUES (?, ?)
    """, (order_id, status))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật trạng thái đơn hàng thành công"
    })