# app/connection.py
import mysql.connector
from app.config import config
import os

# Get environment (default to development)
env = os.getenv('FLASK_ENV', 'development')
cfg = config.get(env, config['default'])


def get_connection():
    """Get MySQL database connection"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'school_db')
        )
        return connection
    except mysql.connector.Error as err:
        if err.errno == 2003:
            print("Error: Cannot connect to MySQL server. Check your database connection settings.")
        elif err.errno == 1045:
            print("Error: Access denied. Check your username and password.")
        else:
            print(f"Error: {err}")
        return None
