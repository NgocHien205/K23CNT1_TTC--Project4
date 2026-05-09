from flask import Blueprint, request, jsonify
from database.db_config import get_connection

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            nd.G9_MaNguoiDung,
            nd.G9_HoTen,
            nd.G9_TenDangNhap,
            nd.G9_Email,
            nd.G9_MaVaiTro,
            vt.G9_TenVaiTro
        FROM G9_NguoiDung nd
        JOIN G9_VaiTro vt ON nd.G9_MaVaiTro = vt.G9_MaVaiTro
        WHERE nd.G9_TenDangNhap = ?
        AND nd.G9_MatKhau = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "success": True,
            "message": "Đăng nhập thành công",
            "user": {
                "id": user.G9_MaNguoiDung,
                "name": user.G9_HoTen,
                "username": user.G9_TenDangNhap,
                "email": user.G9_Email,
                "roleId": user.G9_MaVaiTro,
                "roleName": user.G9_TenVaiTro
            }
        })

    return jsonify({
        "success": False,
        "message": "Sai tài khoản hoặc mật khẩu"
    }), 401