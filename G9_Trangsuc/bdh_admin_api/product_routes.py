from flask import Blueprint, jsonify
from database.db_config import get_connection

product_bp = Blueprint("product_bp", __name__)

@product_bp.route("/", methods=["GET"])
def get_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM G9_SanPham
    """)

    products = []

    for row in cursor.fetchall():

        products.append({
            "id": row.G9_MaSanPham,
            "name": row.G9_TenSanPham,
            "price": float(row.G9_Gia),
            "image": row.G9_HinhAnhChinh
        })

    conn.close()

    return jsonify(products)