# ==============================
# FILE: routes/dashboard_routes.py
# CHỨC NĂNG:
# - Thống kê tổng quan admin
# ==============================

from flask import Blueprint, jsonify
from database.db import get_connection

dashboard_bp = Blueprint("dashboard", __name__)


# ==============================
# API THỐNG KÊ DASHBOARD
# URL: /api/dashboard/
# ==============================
@dashboard_bp.route("/", methods=["GET"])
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    # Đếm sản phẩm
    cursor.execute("SELECT COUNT(*) FROM G9_SanPham")
    total_products = cursor.fetchone()[0]

    # Đếm đơn hàng
    cursor.execute("SELECT COUNT(*) FROM G9_DonHang")
    total_orders = cursor.fetchone()[0]

    # Đếm người dùng
    cursor.execute("SELECT COUNT(*) FROM G9_NguoiDung")
    total_users = cursor.fetchone()[0]

    # Tính doanh thu từ đơn hàng
    cursor.execute("""
        SELECT ISNULL(SUM(G9_TongTien), 0)
        FROM G9_DonHang
    """)
    revenue = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy thống kê thành công",
        "data": {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_users": total_users,
            "revenue": float(revenue)
        }
    })