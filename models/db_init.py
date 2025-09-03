import psycopg2
import os
from urllib.parse import urlparse

def get_db_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise Exception("Bạn cần set biến môi trường DATABASE_URL trước khi chạy!")

    result = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Bảng users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    # Bảng vocab_cards
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vocab_cards (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            image_path TEXT NOT NULL,
            word TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Fix ràng buộc ON DELETE CASCADE nếu chưa có
    cursor.execute("""
        SELECT conname
        FROM pg_constraint
        WHERE conrelid = 'vocab_cards'::regclass
          AND contype = 'f'
    """)
    fk_constraints = cursor.fetchall()
    if fk_constraints:
        fk_name = fk_constraints[0][0]
        cursor.execute(f'ALTER TABLE vocab_cards DROP CONSTRAINT {fk_name}')
        cursor.execute('''
            ALTER TABLE vocab_cards
            ADD CONSTRAINT vocab_cards_user_id_fkey
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ''')

    # Bảng word_info (chứa thông tin mở rộng của từ vựng)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word_info (
            id SERIAL PRIMARY KEY,
            word TEXT UNIQUE NOT NULL,
            phonetic TEXT,
            audio TEXT,
            definition TEXT,
            example TEXT
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Database initialized successfully (users, vocab_cards, word_info).")

if __name__ == '__main__':
    init_db()
