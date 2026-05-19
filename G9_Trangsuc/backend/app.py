from flask import Flask
from flask_cors import CORS

from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.category_routes import category_bp
from routes.order_routes import order_bp
from routes.news_routes import news_bp
from routes.gold_routes import gold_bp
from routes.review_routes import review_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(news_bp, url_prefix="/api/news")
    app.register_blueprint(gold_bp, url_prefix="/api/gold")
    app.register_blueprint(review_bp, url_prefix="/api/reviews")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.route("/")
    def home():
        return {
            "message": "G9 Trang Sức Backend API đang chạy"
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)