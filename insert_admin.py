import sqlite3

conn = sqlite3.connect("company.db")
cursor = conn.cursor()

cursor.execute("""
INSERT OR IGNORE INTO users (username, password, role)
VALUES ('admin', '1234', 'admin')
""")

conn.commit()
conn.close()

print("Admin user created")
