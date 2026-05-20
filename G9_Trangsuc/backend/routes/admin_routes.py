# ==============================
# FILE: routes/admin_routes.py
# CHỨC NĂNG:
# - Quản lý người dùng
# ==============================

from flask import Blueprint, jsonify, request
from database.db import get_connection, rows_to_dict

admin_bp = Blueprint("admin", __name__)


# ==============================
# API LẤY DANH SÁCH NGƯỜI DÙNG
# URL: /api/admin/users
# ==============================
@admin_bp.route("/users", methods=["GET"])
def get_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            nd.G9_MaNguoiDung AS id,
            nd.G9_HoTen AS full_name,
            nd.G9_TenDangNhap AS username,
            nd.G9_Email AS email,
            nd.G9_SoDienThoai AS phone,
            vt.G9_TenVaiTro AS role,
            nd.G9_TrangThai AS status,
            nd.G9_NgayTao AS created_at
        FROM G9_NguoiDung nd
        INNER JOIN G9_VaiTro vt
            ON nd.G9_MaVaiTro = vt.G9_MaVaiTro
        ORDER BY nd.G9_MaNguoiDung DESC
    """)

    users = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy danh sách người dùng thành công",
        "data": users
    })


# ==============================
# API CẬP NHẬT TRẠNG THÁI NGƯỜI DÙNG
# BODY: status
# ==============================
@admin_bp.route("/users/status/<int:user_id>", methods=["PUT"])
def update_user_status(user_id):
    data = request.json
    status = data.get("status")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_NguoiDung
        SET G9_TrangThai = ?
        WHERE G9_MaNguoiDung = ?
    """, (status, user_id))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật trạng thái người dùng thành công"
    })