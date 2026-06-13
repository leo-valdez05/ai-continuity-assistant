import sqlite3
conn = sqlite3.connect("heim.db")
cursor = conn.cursor()
cursor.execute("SELECT concern, user_id FROM concerns ORDER BY id DESC LIMIT 5")
print(cursor.fetchall())
conn.close()