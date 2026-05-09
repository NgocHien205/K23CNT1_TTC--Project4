from flask import Blueprint, request, jsonify
from database.db_config import get_connection

order_bp = Blueprint("order_bp", __name__)

@order_bp.route("/", methods=["GET"])
def get_orders():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            dh.G9_MaDonHang,
            nd.G9_HoTen,
            dh.G9_TenNguoiNhan,
            dh.G9_SDTNhan,
            dh.G9_DiaChiGiao,
            dh.G9_TongTien,
            dh.G9_TrangThai,
            dh.G9_NgayDat
        FROM G9_DonHang dh
        JOIN G9_NguoiDung nd ON dh.G9_MaNguoiDung = nd.G9_MaNguoiDung
        ORDER BY dh.G9_NgayDat DESC
    """)

    orders = []

    for row in cursor.fetchall():
        orders.append({
            "id": row.G9_MaDonHang,
            "customer": row.G9_HoTen,
            "receiver": row.G9_TenNguoiNhan,
            "phone": row.G9_SDTNhan,
            "address": row.G9_DiaChiGiao,
            "total": float(row.G9_TongTien),
            "status": row.G9_TrangThai,
            "createdAt": str(row.G9_NgayDat)
        })

    conn.close()
    return jsonify(orders)


@order_bp.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    cart = data["cart"]

    conn = get_connection()
    cursor = conn.cursor()

    total = sum(item["price"] * item["quantity"] for item in cart)

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
    """, (
        data["userId"],
        data["receiver"],
        data["phone"],
        data["address"],
        total
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
            item["id"],
            item["quantity"],
            item["price"]
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
        data["paymentMethod"],
        total
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Đặt hàng thành công",
        "orderId": order_id
    })