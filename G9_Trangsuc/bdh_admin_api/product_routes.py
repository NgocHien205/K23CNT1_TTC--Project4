from flask import Blueprint, request, jsonify
from database.db_config import get_connection

product_bp = Blueprint("product_bp", __name__)

@product_bp.route("/", methods=["GET"])
def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            sp.G9_MaSanPham,
            sp.G9_TenSanPham,
            sp.G9_ChatLieu,
            sp.G9_Gia,
            sp.G9_SoLuongTon,
            sp.G9_HinhAnhChinh,
            sp.G9_MoTa,
            sp.G9_TrangThai,
            dm.G9_TenDanhMuc
        FROM G9_SanPham sp
        JOIN G9_DanhMuc dm ON sp.G9_MaDanhMuc = dm.G9_MaDanhMuc
    """)

    products = []

    for row in cursor.fetchall():
        products.append({
            "id": row.G9_MaSanPham,
            "name": row.G9_TenSanPham,
            "material": row.G9_ChatLieu,
            "price": float(row.G9_Gia),
            "quantity": row.G9_SoLuongTon,
            "image": row.G9_HinhAnhChinh,
            "description": row.G9_MoTa,
            "status": row.G9_TrangThai,
            "category": row.G9_TenDanhMuc
        })

    conn.close()
    return jsonify(products)


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

    if row:
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

    return jsonify({"message": "Không tìm thấy sản phẩm"}), 404


@product_bp.route("/search/<keyword>", methods=["GET"])
def search_product(keyword):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM G9_SanPham
        WHERE G9_TenSanPham LIKE ?
    """, ('%' + keyword + '%',))

    products = []

    for row in cursor.fetchall():
        products.append({
            "id": row.G9_MaSanPham,
            "name": row.G9_TenSanPham,
            "price": float(row.G9_Gia),
            "image": row.G9_HinhAnhChinh,
            "quantity": row.G9_SoLuongTon
        })

    conn.close()
    return jsonify(products)


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
            G9_MoTa
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["categoryId"],
        data["material"],
        data["price"],
        data["quantity"],
        data["image"],
        data["description"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Thêm sản phẩm thành công"})