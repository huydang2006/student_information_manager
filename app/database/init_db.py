import os
from app.connection import get_connection

def run_sql_file(cursor, filename):
    base_dir = os.path.dirname(__file__)
    filepath = os.path.join(base_dir, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        sql_commands = f.read()

    for command in sql_commands.split(";"):
        cmd = command.strip()
        if cmd:
            cursor.execute(cmd)


def database_has_tables(cursor):
    """Check if database already has tables"""
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return len(tables) > 0


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Nếu database đã có bảng → KHÔNG chạy schema, seed nữa
    if database_has_tables(cursor):
        print("✔ Database already initialized. Skipping schema + seed.")
        cursor.close()
        conn.close()
        return

    # Nếu chưa có bảng → tạo lần đầu
    print("🚀 Initializing database...")
    run_sql_file(cursor, "schema.sql")
    run_sql_file(cursor, "seed.sql")

    conn.commit()
    cursor.close()
    conn.close()
    print("✔ Database initialized successfully.")
