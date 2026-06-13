import sqlite3

conn = sqlite3.connect("heim.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

try:
    cursor.execute("ALTER TABLE conversations ADD COLUMN user_id INTEGER")
except:
    pass

try:
    cursor.execute("ALTER TABLE concerns ADD COLUMN user_id INTEGER")
except:
    pass

try:
    cursor.execute("ALTER TABLE life_events ADD COLUMN user_id INTEGER")
except:
    pass

conn.commit()
conn.close()
print("migration done")