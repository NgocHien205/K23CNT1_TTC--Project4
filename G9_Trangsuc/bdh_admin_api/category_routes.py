from flask import Blueprint, jsonify
from database.db_config import get_connection

# TẠO BLUEPRINT DANH MỤC
category_bp = Blueprint(
    "category_bp",
    __name__
)

# API LẤY DANH SÁCH DANH MỤC
@category_bp.route("/", methods=["GET"])
def get_categories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            G9_MaDanhMuc,
            G9_TenDanhMuc,
            G9_MoTa,
            G9_MaDanhMucCha,
            G9_TrangThai
        FROM G9_DanhMuc
    """)

    categories = []

    rows = cursor.fetchall()

    for row in rows:
        categories.append({
            "id": row.G9_MaDanhMuc,
            "name": row.G9_TenDanhMuc,
            "description": row.G9_MoTa,
            "parentId": row.G9_MaDanhMucCha,
            "status": row.G9_TrangThai
        })

    conn.close()

    return jsonify(categories)