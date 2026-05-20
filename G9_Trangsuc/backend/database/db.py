# ==============================
# FILE: database/db.py
# CHỨC NĂNG:
# - Kết nối SQL Server
# - Chuyển dữ liệu SQL sang dạng dict/json
# ==============================

import pyodbc
import os
from dotenv import load_dotenv

# Load biến môi trường trong file .env
load_dotenv()


# ==============================
# HÀM KẾT NỐI DATABASE
# ==============================
def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    driver = os.getenv("DB_DRIVER")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )

    return pyodbc.connect(conn_str)


# ==============================
# CHUYỂN NHIỀU DÒNG THÀNH LIST DICT
# ==============================
def rows_to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# ==============================
# CHUYỂN 1 DÒNG THÀNH DICT
# ==============================
def row_to_dict(cursor):
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()

    if row:
        return dict(zip(columns, row))

    return None