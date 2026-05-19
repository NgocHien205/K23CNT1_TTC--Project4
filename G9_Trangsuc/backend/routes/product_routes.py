from flask import Blueprint, request, jsonify
from database.db import get_connection

product_bp = Blueprint("product_bp", __name__)


# Lấy tất cả sản phẩm
@product_bp.route("/", methods=["GET"])
def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            sp.G9_MaSanPham,
            sp.G9_TenSanPham,
            sp.G9_MaDanhMuc,
            sp.G9_ChatLieu,
            sp.G9_Gia,
            sp.G9_SoLuongTon,
            sp.G9_HinhAnhChinh,
            sp.G9_MoTa,
            sp.G9_TrangThai,
            dm.G9_TenDanhMuc
        FROM G9_SanPham sp
        JOIN G9_DanhMuc dm
            ON sp.G9_MaDanhMuc = dm.G9_MaDanhMuc
        ORDER BY sp.G9_MaSanPham DESC
    """)

    products = []

    for row in cursor.fetchall():
        products.append({
            "id": row.G9_MaSanPham,
            "name": row.G9_TenSanPham,
            "categoryId": row.G9_MaDanhMuc,
            "category": row.G9_TenDanhMuc,
            "material": row.G9_ChatLieu,
            "price": float(row.G9_Gia),
            "quantity": row.G9_SoLuongTon,
            "image": row.G9_HinhAnhChinh,
            "description": row.G9_MoTa,
            "status": row.G9_TrangThai
        })

    conn.close()
    return jsonify(products)


# Chi tiết sản phẩm
@product_bp.route("/<int:id>", methods=["GET"])
def get_product_detail(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM G9_SanPham
        WHERE G9_MaSanPham = ?
    """, (id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({
            "success": False,
            "message": "Không tìm thấy sản phẩm"
        }), 404

    return jsonify({
        "id": row.G9_MaSanPham,
        "name": row.G9_TenSanPham,
        "categoryId": row.G9_MaDanhMuc,
        "material": row.G9_ChatLieu,
        "price": float(row.G9_Gia),
        "quantity": row.G9_SoLuongTon,
        "image": row.G9_HinhAnhChinh,
        "description": row.G9_MoTa,
        "status": row.G9_TrangThai
    })


# Tìm kiếm sản phẩm
@product_bp.route("/search/<keyword>", methods=["GET"])
def search_products(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM G9_SanPham
        WHERE G9_TenSanPham LIKE ?
    """, (f"%{keyword}%",))

    products = []

    for row in cursor.fetchall():
        products.append({
            "id": row.G9_MaSanPham,
            "name": row.G9_TenSanPham,
            "price": float(row.G9_Gia),
            "quantity": row.G9_SoLuongTon,
            "image": row.G9_HinhAnhChinh,
            "material": row.G9_ChatLieu,
            "status": row.G9_TrangThai
        })

    conn.close()
    return jsonify(products)


# Lọc theo danh mục
@product_bp.route("/category/<int:category_id>", methods=["GET"])
def get_products_by_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM G9_SanPham
        WHERE G9_MaDanhMuc = ?
    """, (category_id,))

    products = []

    for row in cursor.fetchall():
        products.append({
            "id": row.G9_MaSanPham,
            "name": row.G9_TenSanPham,
            "price": float(row.G9_Gia),
            "quantity": row.G9_SoLuongTon,
            "image": row.G9_HinhAnhChinh,
            "material": row.G9_ChatLieu,
            "status": row.G9_TrangThai
        })

    conn.close()
    return jsonify(products)


# Thêm sản phẩm
@product_bp.route("/create", methods=["POST"])
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
            G9_MoTa,
            G9_TrangThai
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("name"),
        data.get("categoryId"),
        data.get("material"),
        data.get("price"),
        data.get("quantity"),
        data.get("image"),
        data.get("description"),
        data.get("status", "Còn hàng")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Thêm sản phẩm thành công"
    })


# Cập nhật sản phẩm
@product_bp.route("/update/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE G9_SanPham
        SET
            G9_TenSanPham = ?,
            G9_MaDanhMuc = ?,
            G9_ChatLieu = ?,
            G9_Gia = ?,
            G9_SoLuongTon = ?,
            G9_HinhAnhChinh = ?,
            G9_MoTa = ?,
            G9_TrangThai = ?
        WHERE G9_MaSanPham = ?
    """, (
        data.get("name"),
        data.get("categoryId"),
        data.get("material"),
        data.get("price"),
        data.get("quantity"),
        data.get("image"),
        data.get("description"),
        data.get("status"),
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Cập nhật sản phẩm thành công"
    })


# Xóa sản phẩm
@product_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_product(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM G9_SanPham
        WHERE G9_MaSanPham = ?
    """, (id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Xóa sản phẩm thành công"
    })