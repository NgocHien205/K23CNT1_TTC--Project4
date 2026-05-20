from flask import Blueprint, jsonify
from database.db import get_connection, rows_to_dict

news_bp = Blueprint("news", __name__)

@news_bp.route("/", methods=["GET"])
def get_news():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            tt.G9_MaTinTuc AS id,
            tt.G9_TieuDe AS title,
            tt.G9_MoTaNgan AS short_description,
            tt.G9_NoiDung AS content,
            tt.G9_HinhAnh AS image,
            tt.G9_NgayDang AS created_at,
            tt.G9_TrangThai AS status,
            dm.G9_TenDanhMuc AS category_name
        FROM G9_TinTuc tt
        LEFT JOIN G9_DanhMucTinTuc dm
            ON tt.G9_MaDanhMuc = dm.G9_MaDanhMuc
        ORDER BY tt.G9_NgayDang DESC
    """)

    news = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy tin tức thành công",
        "data": news
    })