from flask import Blueprint, jsonify

category_bp = Blueprint("categories", __name__)

@category_bp.route("/", methods=["GET"])
def get_categories():
    return jsonify({
        "success": True,
        "message": "Lấy danh mục thành công",
        "data": [
            {"id": 1, "name": "Nhẫn"},
            {"id": 2, "name": "Dây chuyền"},
            {"id": 3, "name": "Bông tai"},
            {"id": 4, "name": "Lắc tay"}
        ]
    })