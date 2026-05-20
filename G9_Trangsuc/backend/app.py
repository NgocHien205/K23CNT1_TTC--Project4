# ==============================
# IMPORT THƯ VIỆN
# ==============================
from flask import Flask
from flask_cors import CORS
import logging
import os

# ==============================
# IMPORT ROUTES
# ==============================
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.category_routes import category_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.news_routes import news_bp
from routes.gold_routes import gold_bp
from routes.review_routes import review_bp
from routes.admin_routes import admin_bp
from routes.dashboard_routes import dashboard_bp

# ==============================
# KHỞI TẠO APP FLASK
# ==============================
app = Flask(__name__)
CORS(app)

# ==============================
# CẤU HÌNH LOG
# ==============================
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

# ==============================
# ĐĂNG KÝ BLUEPRINT ROUTES
# ==============================
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(category_bp, url_prefix="/api/categories")
app.register_blueprint(cart_bp, url_prefix="/api/cart")
app.register_blueprint(order_bp, url_prefix="/api/orders")
app.register_blueprint(news_bp, url_prefix="/api/news")
app.register_blueprint(gold_bp, url_prefix="/api/gold")
app.register_blueprint(review_bp, url_prefix="/api/reviews")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

# ==============================
# ROUTE KIỂM TRA SERVER
# ==============================
@app.route("/")
def home():
    return {
        "success": True,
        "message": "G9 Trang Sức API đang hoạt động"
    }

# ==============================
# CHẠY SERVER
# ==============================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)