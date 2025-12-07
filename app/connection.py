# app/connection.py
import mysql.connector
import os

def get_connection():
    """Create and return MySQL connection (Local + Railway compatible)"""

    host = os.getenv('DB_HOST', 'localhost')
    user = os.getenv('DB_USER', 'root')
    password = os.getenv('DB_PASSWORD', '')
    dbname = os.getenv('DB_NAME', 'school_db')
    # Lưu ý: Cổng mặc định là 3306, Railway có thể dùng cổng khác
    port = int(os.getenv('DB_PORT', 3306))

    # --- KHẮC PHỤC LỖI Ở ĐÂY ---
    # Railway yêu cầu kết nối bảo mật (SSL) cho plugin 'caching_sha2_password'.
    # Ta KHÔNG ĐƯỢC tắt SSL (ssl_disabled=True).
    # Thay vào đó, ta để mặc định để thư viện tự xử lý SSL.
    
    # Cấu hình kết nối
    db_config = {
        'host': host,
        'user': user,
        'password': password,
        'port': port
    }

    # 1) Tạo database nếu chưa tồn tại (chỉ chạy khi cần thiết, bỏ qua lỗi nếu không có quyền)
    try:
        # Kết nối tạm không cần DB name để tạo DB
        temp_conn = mysql.connector.connect(**db_config)
        cur = temp_conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {dbname}")
        cur.close()
        temp_conn.close()
    except Exception as e:
        # Trên Railway thường Database đã có sẵn, lỗi này có thể bỏ qua
        print(f"⚠ Warning (Create DB): {e}")

    # 2) Kết nối DB chính
    try:
        # Thêm tên database vào cấu hình
        db_config['database'] = dbname
        
        # Kết nối chính thức (Mặc định mysql-connector sẽ tự dùng SSL nếu server yêu cầu)
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print("❌ Database connection error:", err)
        return None