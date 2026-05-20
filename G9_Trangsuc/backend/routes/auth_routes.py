# ==============================
# IMPORT THƯ VIỆN
# ==============================
from flask import Blueprint, request, jsonify
from utils.jwt_helper import generate_token

# ==============================
# TẠO BLUEPRINT AUTH
# ==============================
auth_bp = Blueprint("auth", __name__)

# ==============================
# API ĐĂNG NHẬP
# ==============================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    # Tài khoản demo
    if username == "admin" and password == "123456":
        user = {
            "id": 1,
            "username": "admin",
            "role": "admin"
        }

        token = generate_token(user)

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


# ==============================
# API ĐĂNG KÝ
# ==============================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    return jsonify({
        "success": True,
        "message": "Đăng ký thành công",
        "data": data
    })