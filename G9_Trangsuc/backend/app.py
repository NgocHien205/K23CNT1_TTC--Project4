# ==============================
# FILE: app.py
# CHỨC NĂNG:
# - Khởi tạo Flask App
# - Kết nối CORS
# - Đăng ký tất cả API routes
# - Chạy server Flask
# ==============================

from flask import Flask, jsonify
from flask_cors import CORS

# ==============================
# IMPORT ROUTES
# ==============================
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.category_routes import category_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.review_routes import review_bp
from routes.admin_routes import admin_bp
from routes.dashboard_routes import dashboard_bp
from routes.news_routes import news_bp
from routes.gold_routes import gold_bp

# ==============================
# KHỞI TẠO APP
# ==============================
app = Flask(__name__)

# ==============================
# CHO PHÉP FRONTEND GỌI API
# ==============================
CORS(app)

# ==============================
# ROUTE TEST SERVER
# ==============================
@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "G9 Trang Sức API đang hoạt động"
    })


# ==============================
# ĐĂNG KÝ API ROUTES
# ==============================
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(category_bp, url_prefix="/api/categories")
app.register_blueprint(cart_bp, url_prefix="/api/cart")
app.register_blueprint(order_bp, url_prefix="/api/orders")
app.register_blueprint(review_bp, url_prefix="/api/reviews")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
app.register_blueprint(news_bp, url_prefix="/api/news")
app.register_blueprint(gold_bp, url_prefix="/api/gold")


# ==============================
# CHẠY SERVER
# ==============================
if __name__ == "__main__":
    print("===================================")
    print(" G9 TRANG SỨC SERVER ĐANG CHẠY ")
    print(" http://127.0.0.1:5000")
    print("===================================")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )