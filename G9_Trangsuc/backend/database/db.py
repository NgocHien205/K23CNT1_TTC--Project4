# ==============================
# IMPORT THƯ VIỆN
# ==============================
import pymysql
from config import Config

# ==============================
# HÀM KẾT NỐI DATABASE
# ==============================
def get_connection():
    return pymysql.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )