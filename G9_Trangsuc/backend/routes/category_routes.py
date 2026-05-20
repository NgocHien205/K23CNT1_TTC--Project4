from flask import Blueprint, jsonify, request
from database.db import get_connection, rows_to_dict

category_bp = Blueprint("categories", __name__)

# ==============================
# LẤY DANH MỤC
# Bảng: G9_DanhMuc
# ==============================
@category_bp.route("/", methods=["GET"])
def get_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            G9_MaDanhMuc AS id,
            G9_TenDanhMuc AS name,
            G9_MoTa AS description,
            G9_MaDanhMucCha AS parent_id,
            G9_TrangThai AS status
        FROM G9_DanhMuc
        ORDER BY G9_MaDanhMuc DESC
    """)

    categories = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy danh mục thành công",
        "data": categories
    })


# ==============================
# THÊM DANH MỤC
# ==============================
@category_bp.route("/", methods=["POST"])
def create_category():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO G9_DanhMuc
        (
            G9_TenDanhMuc,
            G9_MoTa,
            G9_MaDanhMucCha
        )
        VALUES (?, ?, ?)
    """, (
        data.get("name"),
        data.get("description"),
        data.get("parent_id")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Thêm danh mục thành công"
    })