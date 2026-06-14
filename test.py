


import sqlite3
conn = sqlite3.connect("heim.db")
cursor = conn.cursor()
cursor.execute("SELECT id, username FROM users WHERE username = 'hello_1123'")
print(cursor.fetchone())
conn.close()


import sqlite3
conn = sqlite3.connect("heim.db")
cursor = conn.cursor()
cursor.execute("SELECT concern, user_id FROM concerns WHERE user_id = 8 LIMIT 5")
print(cursor.fetchall())
conn.close()

import sqlite3
conn = sqlite3.connect("heim.db")
cursor = conn.cursor()
cursor.execute("SELECT concern, user_id FROM concerns ORDER BY id DESC LIMIT 5")
print(cursor.fetchall())
conn.close()