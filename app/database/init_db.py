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

        # --- "BỘ LỌC THÔNG MINH" ---
        # 1. Xóa lệnh CREATE DATABASE (để không tạo database lung tung)
        content = re.sub(r"CREATE DATABASE.*?;", "", content, flags=re.IGNORECASE | re.DOTALL)
        
        # 2. Xóa lệnh USE ... (để không bị trỏ nhầm sang school_db)
        content = re.sub(r"USE .*?;", "", content, flags=re.IGNORECASE)

        # 3. Xóa DELIMITER (Python không cần cái này)
        content = re.sub(r"DELIMITER \$\$", "", content, flags=re.IGNORECASE)
        content = re.sub(r"DELIMITER ;", "", content, flags=re.IGNORECASE)

        # Tách lệnh
        commands = content.split(split_by)

        for command in commands:
            cmd = command.strip()
            # Bỏ qua dòng comment hoặc rỗng
            if cmd and not cmd.startswith("--"): 
                try:
                    cursor.execute(cmd)
                    while cursor.nextset(): pass
                except Exception as e:
                    # In lỗi ra để biết nhưng KHÔNG dừng chương trình
                    print(f"   ⚠ Note in {filename}: {e}")
                    
    except FileNotFoundError:
        print(f"   ❌ File not found: {filename}")

def init_database():
    conn = get_connection()
    if conn is None: return

    cursor = conn.cursor()
    
    # Ép chạy lại từ đầu để nạp View/Procedure mới
    print("🚀 Forcing full database initialization (Smart Filter Mode)...")

    # Thứ tự chạy file
    run_sql_file(cursor, "schema.sql", split_by=";")
    run_sql_file(cursor, "seed.sql", split_by=";")
    run_sql_file(cursor, "views.sql", split_by=";")       
    run_sql_file(cursor, "procedures.sql", split_by="$$") 
    run_sql_file(cursor, "triggers.sql", split_by="$$")   

    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Database initialized successfully.")