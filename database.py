import sqlite3

def authenticate(username, password):
    conn = sqlite3.connect("company.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cur.fetchone()

    if user:
        conn.close()
        return True, username, user[0]

    cur.execute(
        "SELECT username FROM computer_users WHERE username=? AND password=?",
        (username, password)
    )
    comp = cur.fetchone()

    if comp:
        conn.close()
        return True, username, "computer_user"

    conn.close()
    return False, None, None
