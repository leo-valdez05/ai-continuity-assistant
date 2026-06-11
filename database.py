import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100),
            created_at DATETIME,
            last_updated DATETIME
        )
    """)

    cursor.execute("""
         CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender VARCHAR(10),
    content TEXT,
    time DATETIME,
    conversation_id INTEGER NOT NULL
     );
     """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concerns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion VARCHAR(50),
    concern VARCHAR(50),
    state VARCHAR(50),
    resolved INTEGER,
    severity VARCHAR(50),
    event_worthy INTEGER,
    is_future_event INTEGER,
    followup_date DATE,
    message TEXT,
    date DATE
    );
                   
   """)
    cursor.execute("""
         CREATE TABLE IF NOT EXISTS life_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotion VARCHAR(50),
    concern VARCHAR(50),
    state VARCHAR(50),
    resolved INTEGER,
    severity VARCHAR(50),
    event_worthy INTEGER,
    is_future_event INTEGER,
    followup_date DATE,
    message TEXT,
    date DATE
    );
    """)

    conn.commit()
    conn.close()




def save_message(conversation_id, sender, content):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (conversation_id, sender, content, time)
        VALUES (?, ?, ?, datetime('now'))
    """, (conversation_id, sender, content))
    conn.commit()
    conn.close()

def create_conversation(title):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (title, created_at, last_updated)
        VALUES (?, datetime('now'), datetime('now'))
    """, (title,))
    conn.commit()
    id = cursor.lastrowid
    conn.close()
    return id

def get_messages(conversation_id):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sender, content FROM messages 
        WHERE conversation_id = ?
        ORDER BY time ASC
    """, (conversation_id,))
    messages = cursor.fetchall()
    conn.close()
    return messages

def get_conversations():
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title FROM conversations
        ORDER BY last_updated DESC
    """)
    conversations = cursor.fetchall()
    conn.close()
    return conversations


if __name__ == "__main__":
    init_db()
    print("database created")
