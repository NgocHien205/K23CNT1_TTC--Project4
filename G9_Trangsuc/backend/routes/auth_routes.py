from flask import Blueprint, request, jsonify
from database.db import get_connection

auth_bp = Blueprint("auth_bp", __name__)


# Đăng nhập
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
            nd.G9_SoDienThoai,
            nd.G9_MaVaiTro,
            nd.G9_TrangThai,
            vt.G9_TenVaiTro
        FROM G9_NguoiDung nd
        JOIN G9_VaiTro vt 
            ON nd.G9_MaVaiTro = vt.G9_MaVaiTro
        WHERE nd.G9_TenDangNhap = ?
        AND nd.G9_MatKhau = ?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({
            "success": False,
            "message": "Sai tài khoản hoặc mật khẩu"
        }), 401

    if user.G9_TrangThai == "Khóa":
        return jsonify({
            "success": False,
            "message": "Tài khoản đã bị khóa"
        }), 403

    return jsonify({
        "success": True,
        "message": "Đăng nhập thành công",
        "user": {
            "id": user.G9_MaNguoiDung,
            "name": user.G9_HoTen,
            "username": user.G9_TenDangNhap,
            "email": user.G9_Email,
            "phone": user.G9_SoDienThoai,
            "roleId": user.G9_MaVaiTro,
            "roleName": user.G9_TenVaiTro
        }
    })


# Đăng ký khách hàng
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT G9_MaNguoiDung
        FROM G9_NguoiDung
        WHERE G9_TenDangNhap = ? OR G9_Email = ?
    """, (
        data.get("username"),
        data.get("email")
    ))

    existed = cursor.fetchone()

    if existed:
        conn.close()
        return jsonify({
            "success": False,
            "message": "Tên đăng nhập hoặc email đã tồn tại"
        }), 400

    cursor.execute("""
        INSERT INTO G9_NguoiDung
        (
            G9_HoTen,
            G9_TenDangNhap,
            G9_MatKhau,
            G9_Email,
            G9_SoDienThoai,
            G9_MaVaiTro
        )
        VALUES (?, ?, ?, ?, ?, 3)
    """, (
        data.get("fullname"),
        data.get("username"),
        data.get("password"),
        data.get("email"),
        data.get("phone")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Đăng ký tài khoản thành công"
    })