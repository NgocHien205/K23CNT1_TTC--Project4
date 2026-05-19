from flask import Blueprint, jsonify, request
from database.db import get_connection

order_bp = Blueprint("order_bp", __name__)


# Lấy danh sách đơn hàng
@order_bp.route("/", methods=["GET"])
def get_orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            dh.G9_MaDonHang,
            nd.G9_HoTen,
            dh.G9_TongTien,
            dh.G9_TrangThai,
            dh.G9_NgayDat
        FROM G9_DonHang dh
        JOIN G9_NguoiDung nd
            ON dh.G9_MaNguoiDung = nd.G9_MaNguoiDung
        ORDER BY dh.G9_MaDonHang DESC
    """)

    orders = []

    for row in cursor.fetchall():

        orders.append({
            "id": row.G9_MaDonHang,
            "customer": row.G9_HoTen,
            "total": float(row.G9_TongTien),
            "status": row.G9_TrangThai,
            "date": str(row.G9_NgayDat)
        })

    conn.close()

    return jsonify(orders)


# Cập nhật trạng thái đơn hàng
@order_bp.route("/update-status/<int:id>", methods=["PUT"])
def update_order_status(id):

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_DonHang
        SET G9_TrangThai = ?
        WHERE G9_MaDonHang = ?
    """, (
        data.get("status"),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật trạng thái đơn hàng thành công"
    })


# Tạo đơn hàng
@order_bp.route("/create", methods=["POST"])
def create_order():
    data = request.json
    cart = data.get("cart", [])

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO G9_DonHang
        (
            G9_MaNguoiDung,
            G9_TenNguoiNhan,
            G9_SDTNhan,
            G9_DiaChiGiao,
            G9_TongTien,
            G9_TrangThai
        )
        OUTPUT INSERTED.G9_MaDonHang
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.get("userId"),
        data.get("receiver"),
        data.get("phone"),
        data.get("address"),
        data.get("total"),
        "Chờ xác nhận"
    ))

    order_id = cursor.fetchone()[0]

    for item in cart:
        cursor.execute("""
            INSERT INTO G9_ChiTietDonHang
            (
                G9_MaDonHang,
                G9_MaSanPham,
                G9_SoLuong,
                G9_DonGia
            )
            VALUES (?, ?, ?, ?)
        """, (
            order_id,
            item.get("id"),
            item.get("quantity"),
            item.get("price")
        ))

    cursor.execute("""
        INSERT INTO G9_ThanhToan
        (
            G9_MaDonHang,
            G9_PhuongThuc,
            G9_SoTien
        )
        VALUES (?, ?, ?)
    """, (
        order_id,
        data.get("paymentMethod"),
        data.get("total")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Đặt hàng thành công",
        "orderId": order_id
    })