import psycopg2
import os
from urllib.parse import urlparse

print(os.getenv('DATABASE_URL'))

def get_db_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise Exception("Bạn cần set biến môi trường DATABASE_URL trước khi chạy!")

    result = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        dbname=result.path[1:],  # bỏ dấu '/'
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tạo bảng users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    # Tạo bảng vocab_cards
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vocab_cards (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            image_path TEXT NOT NULL,
            word TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute(
        "UPDATE users SET role = %s WHERE username = %s",
        ('admin', 'lecuong')
    )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database initialized successfully.")


if __name__ == '__main__':
    init_db()
