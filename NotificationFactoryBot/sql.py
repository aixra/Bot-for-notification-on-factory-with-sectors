import sqlite3


def init_db():
    db = sqlite3.connect("noticeSector.db")
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS noticeSectors (
        user_id INTEGER NOT NULL,
        sector INTEGER NOT NULL,
        message TEXT NOT NULL
    )""")
    db.commit()
    db.close()

def save_message(user_id: int, sector: int, text: str):
    db = sqlite3.connect("noticeSector.db")
    cur = db.cursor()

    cur.execute(
        "INSERT INTO noticeSectors (user_id, sector, message) VALUES (?, ?, ?)",
        (user_id, sector, text)
    )
    db.commit()
    db.close()

def get_all_message():
    db = sqlite3.connect("noticeSector.db")
    cur = db.cursor()

    cur.execute("SELECT user_id, sector, message FROM noticeSectors")
    rows = cur.fetchall()

    db.close()
    return rows



