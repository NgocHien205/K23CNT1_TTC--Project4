from flask import Blueprint, request, jsonify
from database.db import get_connection, row_to_dict
from utils.jwt_helper import generate_token

auth_bp = Blueprint("auth", __name__)

# ==============================
# ĐĂNG NHẬP
# Bảng: G9_NguoiDung + G9_VaiTro
# ==============================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            nd.G9_MaNguoiDung AS id,
            nd.G9_HoTen AS full_name,
            nd.G9_TenDangNhap AS username,
            nd.G9_Email AS email,
            nd.G9_MatKhau AS password,
            vt.G9_TenVaiTro AS role
        FROM G9_NguoiDung nd
        INNER JOIN G9_VaiTro vt 
            ON nd.G9_MaVaiTro = vt.G9_MaVaiTro
        WHERE nd.G9_TenDangNhap = ?
    """, (username,))

    user = row_to_dict(cursor)

    cursor.close()
    conn.close()

    if user and user["password"] == password:
        token = generate_token(user)

        user.pop("password", None)

        return jsonify({
            "success": True,
            "message": "Đăng nhập thành công",
            "token": token,
            "user": user
        })

    return jsonify({
        "success": False,
        "message": "Sai tài khoản hoặc mật khẩu"
    }), 401