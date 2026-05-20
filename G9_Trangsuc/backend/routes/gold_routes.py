from flask import Blueprint, jsonify
from database.db import get_connection, rows_to_dict

gold_bp = Blueprint("gold", __name__)

@gold_bp.route("/", methods=["GET"])
def get_gold_price():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            G9_MaGiaVang AS id,
            G9_LoaiVang AS gold_type,
            G9_GiaMua AS buy_price,
            G9_GiaBan AS sell_price,
            G9_NgayCapNhat AS updated_at
        FROM G9_GiaVang
        ORDER BY G9_NgayCapNhat DESC
    """)

    data = rows_to_dict(cursor)

    cursor.close()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Lấy giá vàng thành công",
        "data": data
    })