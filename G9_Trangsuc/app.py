from flask import Flask
from flask_cors import CORS

from nnh_auth_api.auth_routes import auth_bp
from bdh_admin_api.product_routes import product_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix="/api/nnh/auth")
app.register_blueprint(product_bp, url_prefix="/api/bdh/products")

@app.route("/")
def home():
    return {
        "message": "G9 Trang Suc API Running"
    }

if __name__ == "__main__":
    app.run(debug=True)