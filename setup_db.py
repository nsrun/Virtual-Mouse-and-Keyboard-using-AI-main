import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("company.db")
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# Create computer_users table
cur.execute("""
CREATE TABLE IF NOT EXISTS computer_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    system_id TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# Default admin with hashed password
cur.execute(
    "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
    ("admin", hash_password("admin123"), "admin")
)

conn.commit()
conn.close()

print("Database setup completed")
