import psycopg2.extras
from models.db import get_db_connection

def get_user_by_username_and_password(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        'SELECT * FROM users WHERE username = %s AND password = %s',
        (username, password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        'SELECT * FROM users WHERE username = %s',
        (username,)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def add_user(username, password, role='user'):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
            (username, password, role)
        )
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()
