from flask import Blueprint, jsonify, request
from database.db import get_connection

admin_bp = Blueprint("admin_bp", __name__)


# Dashboard thống kê
@admin_bp.route("/dashboard", methods=["GET"])
def dashboard_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM G9_SanPham")
    products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM G9_DonHang")
    orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM G9_NguoiDung")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM G9_TinTuc")
    news = cursor.fetchone()[0]

    cursor.execute("SELECT ISNULL(SUM(G9_TongTien), 0) FROM G9_DonHang")
    revenue = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "products": products,
        "orders": orders,
        "users": users,
        "news": news,
        "revenue": float(revenue)
    })


# Lấy danh sách người dùng
@admin_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            nd.G9_MaNguoiDung,
            nd.G9_HoTen,
            nd.G9_TenDangNhap,
            nd.G9_Email,
            nd.G9_SoDienThoai,
            nd.G9_TrangThai,
            vt.G9_TenVaiTro
        FROM G9_NguoiDung nd
        JOIN G9_VaiTro vt
            ON nd.G9_MaVaiTro = vt.G9_MaVaiTro
        ORDER BY nd.G9_MaNguoiDung ASC
    """)

    users = []

    for row in cursor.fetchall():
        users.append({
            "id": row.G9_MaNguoiDung,
            "name": row.G9_HoTen,
            "username": row.G9_TenDangNhap,
            "email": row.G9_Email,
            "phone": row.G9_SoDienThoai,
            "status": row.G9_TrangThai,
            "role": row.G9_TenVaiTro
        })

    conn.close()
    return jsonify(users)


# Cập nhật trạng thái người dùng
@admin_bp.route("/users/update-status/<int:id>", methods=["PUT"])
def update_user_status(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_NguoiDung
        SET G9_TrangThai = ?
        WHERE G9_MaNguoiDung = ?
    """, (
        data.get("status"),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật trạng thái người dùng thành công"
    })