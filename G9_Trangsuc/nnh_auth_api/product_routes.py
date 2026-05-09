@product_bp.route("/<int:id>", methods=["GET"])
def get_product_detail(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM G9_SanPham
        WHERE G9_MaSanPham = ?
    """, (id))

    row = cursor.fetchone()

    conn.close()

    if row:

        return jsonify({
            "id": row.G9_MaSanPham,
            "name": row.G9_TenSanPham,
            "price": float(row.G9_Gia),
            "image": row.G9_HinhAnhChinh,
            "description": row.G9_MoTa,
            "quantity": row.G9_SoLuongTon
        })

    return jsonify({
        "message": "Không tìm thấy sản phẩm"
    })