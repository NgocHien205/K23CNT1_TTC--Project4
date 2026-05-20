from flask import Blueprint, jsonify

news_bp = Blueprint("news", __name__)

@news_bp.route("/", methods=["GET"])
def get_news():
    return jsonify({
        "success": True,
        "message": "Lấy tin tức thành công",
        "data": [
            {
                "id": 1,
                "title": "Xu hướng trang sức 2026",
                "content": "Các mẫu trang sức vàng, bạc đang được yêu thích."
            }
        ]
    })