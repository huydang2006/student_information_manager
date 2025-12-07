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
        
        # Xử lý DELIMITER để Python hiểu được
        content = re.sub(r"DELIMITER \$\$", "", content, flags=re.IGNORECASE)
        content = re.sub(r"DELIMITER ;", "", content, flags=re.IGNORECASE)
        content = re.sub(r"USE school_db;", "", content, flags=re.IGNORECASE)

        commands = content.split(split_by)
        for command in commands:
            cmd = command.strip()
            if cmd and not cmd.startswith("--"): 
                try:
                    cursor.execute(cmd)
                    while cursor.nextset(): pass
                except Exception as e:
                    print(f"   ⚠ Note in {filename}: {e}")
                    
    except FileNotFoundError:
        print(f"   ❌ File not found: {filename}")

def init_database():
    conn = get_connection()
    if conn is None: return

    cursor = conn.cursor()
    
    # --- DÒNG QUAN TRỌNG NHẤT: BẮT BUỘC CHẠY LẠI TỪ ĐẦU ---
    print("🚀 Forcing full database initialization...") 

    # Chạy lần lượt các file
    run_sql_file(cursor, "schema.sql", split_by=";")
    run_sql_file(cursor, "seed.sql", split_by=";")
    run_sql_file(cursor, "views.sql", split_by=";")       # <-- Phải có dòng này
    run_sql_file(cursor, "procedures.sql", split_by="$$") # <-- Phải có dòng này
    run_sql_file(cursor, "triggers.sql", split_by="$$")   # <-- Phải có dòng này

    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Database reset & initialized successfully.")