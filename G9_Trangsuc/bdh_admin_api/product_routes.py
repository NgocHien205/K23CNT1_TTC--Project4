from flask import Blueprint, jsonify
from database.db_config import get_connection

# TẠO BLUEPRINT
product_bp = Blueprint(
    "product_bp",
    __name__
)

# API LẤY DANH SÁCH SẢN PHẨM
@product_bp.route("/", methods=["GET"])
def get_products():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM G9_SanPham
    """)

    products = []

    rows = cursor.fetchall()

    for row in rows:

        products.append({

            "id": row.G9_MaSanPham,
            "name": row.G9_TenSanPham,
            "price": float(row.G9_Gia),
            "image": row.G9_HinhAnhChinh,
            "quantity": row.G9_SoLuongTon

        })

    conn.close()

    return jsonify(products)