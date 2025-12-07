import os
from app.connection import get_connection

def run_sql_file(cursor, filename, split_by=";"):
    base_dir = os.path.dirname(__file__)
    filepath = os.path.join(base_dir, filename)
    print(f"   ... Processing {filename}")
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # --- BƯỚC 1: LỌC SẠCH FILE (LINE BY LINE) ---
        clean_lines = []
        for line in lines:
            stripped = line.strip()
            upper_line = stripped.upper()

            # Bỏ qua dòng comment
            if stripped.startswith("--"):
                continue
            
            # Bỏ qua lệnh chuyển Database (Nguyên nhân gây lỗi)
            if upper_line.startswith("USE ") or upper_line.startswith("CREATE DATABASE"):
                continue
                
            # Bỏ qua lệnh DELIMITER (Python không cần)
            if upper_line.startswith("DELIMITER"):
                continue

            clean_lines.append(line)

        # Ghép lại thành một chuỗi sạch sẽ
        content = "".join(clean_lines)

        # --- BƯỚC 2: CHẠY LỆNH ---
        commands = content.split(split_by)

        for command in commands:
            if command.strip(): # Chỉ chạy nếu lệnh không rỗng
                try:
                    cursor.execute(command)
                    while cursor.nextset(): pass
                except Exception as e:
                    # In lỗi warning nhưng không dừng chương trình
                    # (Ví dụ: Lỗi bảng đã tồn tại thì cứ kệ nó)
                    print(f"   ⚠ Note in {filename}: {e}")

    except FileNotFoundError:
        print(f"   ❌ File not found: {filename}")

def init_database():
    conn = get_connection()
    if conn is None: return

    cursor = conn.cursor()
    print("🚀 Forcing full database initialization (Final Fix)...")

    # Thứ tự chạy file: Schema -> Seed -> Views -> Procedures -> Triggers
    run_sql_file(cursor, "schema.sql", split_by=";")
    run_sql_file(cursor, "seed.sql", split_by=";")
    run_sql_file(cursor, "views.sql", split_by=";")       
    
    # Procedure và Trigger tách bằng $$
    run_sql_file(cursor, "procedures.sql", split_by="$$") 
    run_sql_file(cursor, "triggers.sql", split_by="$$")   

    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Database initialized successfully.")