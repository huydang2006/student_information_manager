import os
import re
from app.connection import get_connection

def run_sql_file(cursor, filename, split_by=";"):
    base_dir = os.path.dirname(__file__)
    filepath = os.path.join(base_dir, filename)

    print(f"   ... Executing {filename}")
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Loại bỏ dòng DELIMITER (Python không cần lệnh này)
        content = re.sub(r"DELIMITER \$\$", "", content, flags=re.IGNORECASE)
        content = re.sub(r"DELIMITER ;", "", content, flags=re.IGNORECASE)

        # Tách lệnh dựa trên dấu phân cách được chỉ định
        commands = content.split(split_by)

        for command in commands:
            cmd = command.strip()
            # Bỏ qua các lệnh rỗng hoặc chỉ có comments
            if cmd and not cmd.startswith("--"): 
                try:
                    cursor.execute(cmd)
                    # Cần thiết cho Procedures/Triggers để tránh lỗi "Commands out of sync"
                    while cursor.nextset():
                        pass
                except Exception as e:
                    print(f"   ⚠ Error in {filename}: {e}")
                    # Không return ở đây để cố chạy tiếp các lệnh khác
                    
    except FileNotFoundError:
        print(f"   ❌ File not found: {filename}")

def database_is_empty(cursor):
    """Kiểm tra xem database có bảng payment chưa (dấu hiệu đã init)"""
    try:
        cursor.execute("SHOW TABLES LIKE 'payment'")
        result = cursor.fetchone()
        return result is None
    except:
        return True

def init_database():
    conn = get_connection()
    if conn is None:
        print("❌ Could not connect to database.")
        return

    cursor = conn.cursor()

    # Kiểm tra xem có cần chạy lại từ đầu không
    # Mẹo: Nếu bảng 'payment' chưa có, tức là DB mới tinh -> Chạy hết
    if not database_is_empty(cursor):
        print("✔ Database tables execute. Skipping initialization.")
        cursor.close()
        conn.close()
        return

    print("🚀 Initializing full database structure...")

    # 1. Tạo bảng (Schema) - Tách bằng ;
    run_sql_file(cursor, "schema.sql", split_by=";")

    # 2. Thêm dữ liệu mẫu (Seed) - Tách bằng ;
    run_sql_file(cursor, "seed.sql", split_by=";")

    # 3. Tạo Views - Tách bằng ;
    run_sql_file(cursor, "views.sql", split_by=";")

    # 4. Tạo Procedures - Tách bằng $$ (QUAN TRỌNG)
    run_sql_file(cursor, "procedures.sql", split_by="$$")

    # 5. Tạo Triggers - Tách bằng $$ (QUAN TRỌNG)
    run_sql_file(cursor, "triggers.sql", split_by="$$")

    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Database initialized successfully (Full 5 files).")