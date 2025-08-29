# db.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    """
    Returns a new MySQL connection. Edit the credentials below or
    set appropriate environment variables in your environment instead.
    """
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",              # <-- change if needed
            password="server", # <-- change if needed
            database="hotel_db"
        )
    except Error as e:
        raise RuntimeError(f"Could not connect to DB: {e}")
