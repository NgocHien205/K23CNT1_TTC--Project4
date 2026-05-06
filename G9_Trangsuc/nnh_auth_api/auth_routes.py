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
        SELECT *
        FROM G9_NguoiDung
        WHERE G9_TenDangNhap = ?
        AND G9_MatKhau = ?
    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({
            "message": "Đăng nhập thành công"
        })

    return jsonify({
        "message": "Sai tài khoản hoặc mật khẩu"
    }), 401