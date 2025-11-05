import os, psycopg2, bcrypt, pandas as pd
from datetime import datetime

def get_conn():
    return psycopg2.connect(
        host=os.getenv('PGHOST'),
        port=os.getenv('PGPORT', '5432'),
        dbname=os.getenv('PGDATABASE'),
        user=os.getenv('PGUSER'),
        password=os.getenv('PGPASSWORD')
    )

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );''')
    cur.execute('''CREATE TABLE IF NOT EXISTS progress (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        module TEXT,
        score FLOAT,
        details TEXT,
        timestamp TIMESTAMP DEFAULT NOW()
    );''')
    conn.commit()
    cur.close()
    conn.close()

def login_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username=%s;", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row and bcrypt.checkpw(password.encode(), row[0].encode()):
        return True
    return False

def register_user(username, password):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=%s;", (username,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return False
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cur.execute("INSERT INTO users (username, password_hash) VALUES (%s,%s);", (username, pw_hash))
    conn.commit()
    cur.close()
    conn.close()
    return True

def get_user_id(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=%s;", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

def save_progress(username, module, score, details):
    uid = get_user_id(username)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO progress (user_id,module,score,details) VALUES (%s,%s,%s,%s);",
                (uid, module, score, str(details)[:1000]))
    conn.commit()
    cur.close()
    conn.close()

def get_user_progress(username):
    uid = get_user_id(username)
    conn = get_conn()
    df = pd.read_sql("SELECT module,score,timestamp FROM progress WHERE user_id=%s ORDER BY timestamp DESC;", conn, params=(uid,))
    conn.close()
    return df
