# print_db_tables.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # load DATABASE_URL từ file .env nếu có


def get_db_connection():
    """
    Kết nối PostgreSQL từ URL.
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise Exception("Bạn cần set biến môi trường DATABASE_URL hoặc file .env!")

    conn = psycopg2.connect(DATABASE_URL)
    return conn


def print_table_data(conn, table_name):
    cur = conn.cursor()

    # Lấy danh sách cột
    cur.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = %s
        ORDER BY ordinal_position;
    """, (table_name,))
    columns = [col[0] for col in cur.fetchall()]

    # Lấy toàn bộ dữ liệu trong bảng
    cur.execute(f"SELECT * FROM {table_name};")
    rows = cur.fetchall()

    print(f"\n📌 Bảng: {table_name}")
    print("   Các cột:", columns)
    if rows:
        for row in rows:
            record = dict(zip(columns, row))
            print("   ➝", record)
    else:
        print("   (Bảng trống)")

    cur.close()


# ========================
# MAIN
# ========================
if __name__ == "__main__":
    conn = get_db_connection()
    cur = conn.cursor()

    # Lấy tất cả các bảng trong schema public
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='public'
        ORDER BY table_name;
    """)
    tables = [t[0] for t in cur.fetchall()]
    cur.close()

    print("📂 Danh sách bảng:", tables)

    # In dữ liệu từng bảng (full)
    for table in tables:
        print_table_data(conn, table)

    conn.close()
