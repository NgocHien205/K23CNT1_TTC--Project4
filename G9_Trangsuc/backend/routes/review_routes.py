# ==============================
# FILE: routes/review_routes.py
# CHỨC NĂNG:
# - Lấy đánh giá theo sản phẩm
# - Thêm đánh giá sản phẩm
# ==============================

from flask import Blueprint, jsonify, request
from database.db import get_connection, rows_to_dict

review_bp = Blueprint("reviews", __name__)


# ==============================
# API LẤY ĐÁNH GIÁ THEO SẢN PHẨM
# URL: /api/reviews/product/1
# ==============================
@review_bp.route("/product/<int:product_id>", methods=["GET"])
def get_reviews_by_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            dg.G9_MaDanhGia AS id,
            nd.G9_HoTen AS full_name,
            dg.G9_SoSao AS rating,
            dg.G9_NoiDung AS content,
            dg.G9_TrangThai AS status,
            dg.G9_NgayDanhGia AS created_at
        FROM G9_DanhGia dg
        INNER JOIN G9_NguoiDung nd
            ON dg.G9_MaNguoiDung = nd.G9_MaNguoiDung
        WHERE dg.G9_MaSanPham = ?
        ORDER BY dg.G9_MaDanhGia DESC
    """, (product_id,))

    data = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy đánh giá thành công",
        "data": data
    })


# ==============================
# API THÊM ĐÁNH GIÁ
# BODY: product_id, user_id, rating, content
# ==============================
@review_bp.route("/", methods=["POST"])
def create_review():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO G9_DanhGia
        (
            G9_MaSanPham,
            G9_MaNguoiDung,
            G9_SoSao,
            G9_NoiDung
        )
        VALUES (?, ?, ?, ?)
    """, (
        data.get("product_id"),
        data.get("user_id"),
        data.get("rating"),
        data.get("content")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Đánh giá sản phẩm thành công"
    })