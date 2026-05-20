# ==============================
# IMPORT THƯ VIỆN
# ==============================
import jwt
import datetime
from config import Config

# ==============================
# TẠO TOKEN ĐĂNG NHẬP
# ==============================
def generate_token(user):
    payload = {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    return token

# ==============================
# GIẢI MÃ TOKEN
# ==============================
def decode_token(token):
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
    except:
        return None