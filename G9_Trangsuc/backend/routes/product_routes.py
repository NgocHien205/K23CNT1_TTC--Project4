from flask import Blueprint, jsonify, request
from database.db import get_connection, rows_to_dict, row_to_dict

product_bp = Blueprint("products", __name__)

# ==============================
# LẤY DANH SÁCH SẢN PHẨM
# Bảng: G9_SanPham
# ==============================
@product_bp.route("/", methods=["GET"])
def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            sp.G9_MaSanPham AS id,
            sp.G9_TenSanPham AS name,
            sp.G9_Gia AS price,
            sp.G9_SoLuongTon AS quantity,
            sp.G9_HinhAnhChinh AS image,
            sp.G9_MoTa AS description,
            sp.G9_ChatLieu AS material,
            sp.G9_TrangThai AS status,
            dm.G9_TenDanhMuc AS category_name
        FROM G9_SanPham sp
        LEFT JOIN G9_DanhMuc dm 
            ON sp.G9_MaDanhMuc = dm.G9_MaDanhMuc
        ORDER BY sp.G9_MaSanPham DESC
    """)

    products = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy danh sách sản phẩm thành công",
        "data": products
    })


# ==============================
# LẤY CHI TIẾT SẢN PHẨM
# ==============================
@product_bp.route("/<int:id>", methods=["GET"])
def get_product_detail(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            sp.G9_MaSanPham AS id,
            sp.G9_TenSanPham AS name,
            sp.G9_Gia AS price,
            sp.G9_SoLuongTon AS quantity,
            sp.G9_HinhAnhChinh AS image,
            sp.G9_MoTa AS description,
            sp.G9_ChatLieu AS material,
            sp.G9_TrangThai AS status,
            dm.G9_TenDanhMuc AS category_name
        FROM G9_SanPham sp
        LEFT JOIN G9_DanhMuc dm 
            ON sp.G9_MaDanhMuc = dm.G9_MaDanhMuc
        WHERE sp.G9_MaSanPham = ?
    """, (id,))

    product = row_to_dict(cursor)

    cursor.close()
    conn.close()

    if product:
        return jsonify({
            "success": True,
            "message": "Lấy chi tiết sản phẩm thành công",
            "data": product
        })

    return jsonify({
        "success": False,
        "message": "Không tìm thấy sản phẩm"
    }), 404


# ==============================
# THÊM SẢN PHẨM
# ==============================
@product_bp.route("/", methods=["POST"])
def create_product():
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO G9_SanPham
        (
            G9_TenSanPham,
            G9_MaDanhMuc,
            G9_ChatLieu,
            G9_Gia,
            G9_SoLuongTon,
            G9_HinhAnhChinh,
            G9_MoTa
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("name"),
        data.get("category_id"),
        data.get("material"),
        data.get("price"),
        data.get("quantity"),
        data.get("image"),
        data.get("description")
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Thêm sản phẩm thành công"
    })