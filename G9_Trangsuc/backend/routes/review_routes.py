from flask import Blueprint, jsonify, request

review_bp = Blueprint("reviews", __name__)

reviews = []

@review_bp.route("/", methods=["GET"])
def get_reviews():
    return jsonify({
        "success": True,
        "message": "Lấy đánh giá thành công",
        "data": reviews
    })

@review_bp.route("/", methods=["POST"])
def create_review():
    data = request.json
    reviews.append(data)

    return jsonify({
        "success": True,
        "message": "Thêm đánh giá thành công",
        "data": data
    })