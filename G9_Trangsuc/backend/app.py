from flask import Flask
from flask_cors import CORS

from backend.nnh_auth_api.auth_routes import auth_bp
from backend.routes.product_routes import product_bp
from backend.routes.category_routes import category_bp
from backend.routes.order_routes import order_bp
from backend.routes.gold_routes import gold_bp
from backend.routes.news_routes import news_bp
from backend.routes.dashboard_routes import dashboard_bp
from backend.routes.user_routes import user_bp
from backend.routes.review_routes import review_bp
from backend.routes.upload_routes import upload_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api/nnh/auth")
app.register_blueprint(product_bp, url_prefix="/api/bdh/products")
app.register_blueprint(category_bp, url_prefix="/api/bdh/categories")
app.register_blueprint(order_bp, url_prefix="/api/bdh/orders")
app.register_blueprint(gold_bp, url_prefix="/api/bdh/gold")
app.register_blueprint(news_bp, url_prefix="/api/bdh/news")
app.register_blueprint(dashboard_bp, url_prefix="/api/bdh/dashboard")
app.register_blueprint(user_bp, url_prefix="/api/bdh/users")
app.register_blueprint(review_bp, url_prefix="/api/bdh/reviews")
app.register_blueprint(upload_bp,url_prefix="/api/bdh/upload")
    

@app.route("/")
def home():
    return {
        "message": "G9 Trang Sức API đang chạy"
    }

if __name__ == "__main__":
    app.run(debug=True)