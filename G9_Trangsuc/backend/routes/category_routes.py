from flask import Blueprint, request, jsonify
from database.db import get_connection

category_bp = Blueprint("category_bp", __name__)


# Lấy danh mục
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
        ORDER BY G9_MaDanhMuc ASC
    """)

    categories = []

    for row in cursor.fetchall():
        categories.append({
            "id": row.G9_MaDanhMuc,
            "name": row.G9_TenDanhMuc,
            "description": row.G9_MoTa,
            "parentId": row.G9_MaDanhMucCha,
            "status": row.G9_TrangThai
        })

    conn.close()
    return jsonify(categories)


# Thêm danh mục
@category_bp.route("/create", methods=["POST"])
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
        data.get("parentId"),
        data.get("status", "Hoạt động")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Thêm danh mục thành công"
    })


# Cập nhật danh mục
@category_bp.route("/update/<int:id>", methods=["PUT"])
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
        data.get("parentId"),
        data.get("status"),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật danh mục thành công"
    })


# Ẩn / hiện danh mục
@category_bp.route("/update-status/<int:id>", methods=["PUT"])
def update_category_status(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_DanhMuc
        SET G9_TrangThai = ?
        WHERE G9_MaDanhMuc = ?
    """, (
        data.get("status"),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật trạng thái danh mục thành công"
    })


# Xóa danh mục
@category_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_category(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM G9_DanhMuc
        WHERE G9_MaDanhMuc = ?
    """, (id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Xóa danh mục thành công"
    })