# ==============================
# FILE: routes/category_routes.py
# CHỨC NĂNG:
# - Lấy danh mục
# - Thêm danh mục
# - Cập nhật danh mục
# - Xóa danh mục
# ==============================

from flask import Blueprint, jsonify, request
from database.db import get_connection, rows_to_dict

category_bp = Blueprint("categories", __name__)


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
            G9_MaDanhMucCha,
            G9_TrangThai
        )
        VALUES (?, ?, ?, ?)
    """, (
        data.get("name"),
        data.get("description"),
        data.get("parent_id") or None,
        data.get("status", "Hoạt động")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Thêm danh mục thành công"
    })


@category_bp.route("/<int:id>", methods=["PUT"])
def update_category(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_DanhMuc
        SET 
            G9_TenDanhMuc = ?,
            G9_MoTa = ?,
            G9_MaDanhMucCha = ?,
            G9_TrangThai = ?
        WHERE G9_MaDanhMuc = ?
    """, (
        data.get("name"),
        data.get("description"),
        data.get("parent_id") or None,
        data.get("status"),
        id
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật danh mục thành công"
    })


@category_bp.route("/<int:id>", methods=["DELETE"])
def delete_category(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM G9_DanhMuc
        WHERE G9_MaDanhMuc = ?
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Xóa danh mục thành công"
    })