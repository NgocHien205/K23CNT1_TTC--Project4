from flask import Blueprint, jsonify, request
from database.db_config import get_connection

# TẠO BLUEPRINT
order_bp = Blueprint(
    "order_bp",
    __name__
)

# LẤY DANH SÁCH ĐƠN HÀNG
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
    """)

    orders = []

    rows = cursor.fetchall()

    for row in rows:

        orders.append({

            "id": row.G9_MaDonHang,
            "customer": row.G9_HoTen,
            "total": float(row.G9_TongTien),
            "status": row.G9_TrangThai,
            "date": str(row.G9_NgayDat)

        })

    conn.close()

    return jsonify(orders)


# ĐẶT HÀNG
@order_bp.route("/checkout", methods=["POST"])
def checkout():

    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO G9_DonHang
        (
            G9_MaNguoiDung,
            G9_TenNguoiNhan,
            G9_SDTNhan,
            G9_DiaChiGiao,
            G9_TongTien
        )

        VALUES (?, ?, ?, ?, ?)
    """, (

        data["userId"],
        data["receiver"],
        data["phone"],
        data["address"],
        data["total"]

    ))

    conn.commit()

    conn.close()

    return jsonify({

        "success": True,
        "message": "Đặt hàng thành công"

    })