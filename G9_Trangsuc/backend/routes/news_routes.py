from flask import Blueprint, jsonify, request
from database.db import get_connection

news_bp = Blueprint("news_bp", __name__)


# Lấy danh sách tin tức
@news_bp.route("/", methods=["GET"])
def get_news():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            tt.G9_MaTinTuc,
            tt.G9_TieuDe,
            tt.G9_MoTaNgan,
            tt.G9_NoiDung,
            tt.G9_HinhAnh,
            tt.G9_NgayDang,
            tt.G9_TrangThai,
            dm.G9_TenDanhMuc,
            nd.G9_HoTen
        FROM G9_TinTuc tt
        LEFT JOIN G9_DanhMucTinTuc dm
            ON tt.G9_MaDanhMuc = dm.G9_MaDanhMuc
        LEFT JOIN G9_NguoiDung nd
            ON tt.G9_MaNguoiDang = nd.G9_MaNguoiDung
        ORDER BY tt.G9_NgayDang DESC
    """)

    news_list = []

    for row in cursor.fetchall():
        news_list.append({
            "id": row.G9_MaTinTuc,
            "title": row.G9_TieuDe,
            "shortDescription": row.G9_MoTaNgan,
            "content": row.G9_NoiDung,
            "image": row.G9_HinhAnh,
            "createdAt": str(row.G9_NgayDang),
            "status": row.G9_TrangThai,
            "category": row.G9_TenDanhMuc,
            "author": row.G9_HoTen
        })

    conn.close()
    return jsonify(news_list)


# Chi tiết tin tức
@news_bp.route("/<int:id>", methods=["GET"])
def get_news_detail(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            G9_MaTinTuc,
            G9_TieuDe,
            G9_MoTaNgan,
            G9_NoiDung,
            G9_HinhAnh,
            G9_NgayDang,
            G9_TrangThai
        FROM G9_TinTuc
        WHERE G9_MaTinTuc = ?
    """, (id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({
            "success": False,
            "message": "Không tìm thấy tin tức"
        }), 404

    return jsonify({
        "id": row.G9_MaTinTuc,
        "title": row.G9_TieuDe,
        "shortDescription": row.G9_MoTaNgan,
        "content": row.G9_NoiDung,
        "image": row.G9_HinhAnh,
        "createdAt": str(row.G9_NgayDang),
        "status": row.G9_TrangThai
    })


# Lấy danh mục tin tức
@news_bp.route("/categories", methods=["GET"])
def get_news_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            G9_MaDanhMuc,
            G9_TenDanhMuc
        FROM G9_DanhMucTinTuc
    """)

    categories = []

    for row in cursor.fetchall():
        categories.append({
            "id": row.G9_MaDanhMuc,
            "name": row.G9_TenDanhMuc
        })

    conn.close()
    return jsonify(categories)


# Thêm tin tức
@news_bp.route("/create", methods=["POST"])
def create_news():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO G9_TinTuc
        (
            G9_TieuDe,
            G9_MoTaNgan,
            G9_NoiDung,
            G9_HinhAnh,
            G9_MaNguoiDang,
            G9_MaDanhMuc,
            G9_TrangThai
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("title"),
        data.get("shortDescription"),
        data.get("content"),
        data.get("image"),
        data.get("userId"),
        data.get("categoryId"),
        data.get("status", "Hiển thị")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Thêm tin tức thành công"
    })


# Cập nhật tin tức
@news_bp.route("/update/<int:id>", methods=["PUT"])
def update_news(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_TinTuc
        SET
            G9_TieuDe = ?,
            G9_MoTaNgan = ?,
            G9_NoiDung = ?,
            G9_HinhAnh = ?,
            G9_MaDanhMuc = ?,
            G9_TrangThai = ?
        WHERE G9_MaTinTuc = ?
    """, (
        data.get("title"),
        data.get("shortDescription"),
        data.get("content"),
        data.get("image"),
        data.get("categoryId"),
        data.get("status"),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật tin tức thành công"
    })


# Ẩn / hiện tin tức
@news_bp.route("/update-status/<int:id>", methods=["PUT"])
def update_news_status(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_TinTuc
        SET G9_TrangThai = ?
        WHERE G9_MaTinTuc = ?
    """, (
        data.get("status"),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật trạng thái tin tức thành công"
    })


# Xóa tin tức
@news_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_news(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM G9_TinTuc
        WHERE G9_MaTinTuc = ?
    """, (id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Xóa tin tức thành công"
    })