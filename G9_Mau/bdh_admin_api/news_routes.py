# Import các thư viện cần dùng
from flask import Blueprint, jsonify, request
from database.db_config import get_connection


# =========================================================
# TẠO BLUEPRINT CHO MODULE TIN TỨC
# Blueprint giúp tách riêng API tin tức ra khỏi app.py
# =========================================================
news_bp = Blueprint("news_bp", __name__)


# =========================================================
# 1. API LẤY DANH SÁCH TIN TỨC
# URL: GET /api/bdh/news/
# Dùng cho:
# - Trang admin quản lý tin tức
# - Trang khách hàng xem danh sách tin tức
# =========================================================
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


# =========================================================
# 2. API LẤY CHI TIẾT TIN TỨC
# URL: GET /api/bdh/news/<id>
# Dùng cho trang news-detail.html
# =========================================================
@news_bp.route("/<int:id>", methods=["GET"])
def get_news_detail(id):
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

        WHERE tt.G9_MaTinTuc = ?
    """, (id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return jsonify({
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

    return jsonify({
        "success": False,
        "message": "Không tìm thấy tin tức"
    }), 404


# =========================================================
# 3. API LẤY DANH SÁCH DANH MỤC TIN TỨC
# URL: GET /api/bdh/news/categories
# Dùng để đổ dữ liệu vào select danh mục khi thêm/sửa tin tức
# =========================================================
@news_bp.route("/categories", methods=["GET"])
def get_news_categories():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            G9_MaDanhMuc,
            G9_TenDanhMuc
        FROM G9_DanhMucTinTuc
        ORDER BY G9_MaDanhMuc ASC
    """)

    categories = []

    for row in cursor.fetchall():
        categories.append({
            "id": row.G9_MaDanhMuc,
            "name": row.G9_TenDanhMuc
        })

    conn.close()

    return jsonify(categories)


# =========================================================
# 4. API THÊM TIN TỨC
# URL: POST /api/bdh/news/create
# Dữ liệu nhận từ frontend:
# title, shortDescription, content, image, userId, categoryId, status
# =========================================================
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


# =========================================================
# 5. API CẬP NHẬT TIN TỨC
# URL: PUT /api/bdh/news/update/<id>
# Dùng khi admin bấm Sửa và Lưu tin tức
# =========================================================
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
        data.get("status", "Hiển thị"),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật tin tức thành công"
    })


# =========================================================
# 6. API CẬP NHẬT TRẠNG THÁI TIN TỨC
# URL: PUT /api/bdh/news/update-status/<id>
# Dùng để Ẩn / Hiển thị tin tức
# =========================================================
@news_bp.route("/update-status/<int:id>", methods=["PUT"])
def update_news_status(id):
    data = request.json
    status = data.get("status")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_TinTuc
        SET G9_TrangThai = ?
        WHERE G9_MaTinTuc = ?
    """, (
        status,
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật trạng thái tin tức thành công"
    })


# =========================================================
# 7. API XÓA TIN TỨC
# URL: DELETE /api/bdh/news/delete/<id>
# Dùng khi admin muốn xóa tin tức khỏi database
# =========================================================
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