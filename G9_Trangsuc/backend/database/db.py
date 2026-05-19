import pyodbc
from config import Config


def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={Config.DB_DRIVER};"
        f"SERVER={Config.DB_SERVER};"
        f"DATABASE={Config.DB_NAME};"
        f"Trusted_Connection={Config.DB_TRUSTED_CONNECTION};"
    )

    return conn