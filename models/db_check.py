import psycopg2

def print_table_data(conn, table_name):
    cur = conn.cursor()

    # Lấy danh sách cột
    cur.execute(f"""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
    """)
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
conn = psycopg2.connect(
    "postgresql://lecuong:eWHFyeAV6NhQOTNhr8OFTooRE6v4IM2g@dpg-d2blo6buibrs73fo0o00-a.singapore-postgres.render.com/mydatabase_ri2s"
)
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


