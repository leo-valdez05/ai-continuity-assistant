import sqlite3
from datetime import datetime, timedelta
import os
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "heim.db")


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

def create_conversation(title, user_id):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO conversations (title, created_at, last_updated, user_id)
        VALUES (?, datetime('now'), datetime('now'), ?)
    """, (title, user_id))
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

def get_conversations(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("DB_PATH:", DB_PATH)
    print("querying with user_id:", user_id, type(user_id))
    cursor.execute("""
        SELECT id, title FROM conversations
        WHERE user_id = ?
        ORDER BY last_updated DESC
    """, (user_id,))
    conversations = cursor.fetchall()
    print("raw result:", conversations)
    conn.close()
    return conversations

def update_conversation_title(conversation_id, title):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE conversations SET title = ?, last_updated = datetime('now')
        WHERE id = ?
    """, (title[:50], conversation_id))
    conn.commit()
    conn.close()

def save_concern(detector):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO concerns (emotion, concern, state, resolved, severity, 
        event_worthy, is_future_event, followup_date, message, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        detector.get("emotion"),
        detector.get("concern"),
        detector.get("state"),
        1 if detector.get("resolved") else 0,
        detector.get("severity"),
        1 if detector.get("event_worthy") else 0,
        1 if detector.get("is_future_event") else 0,
        detector.get("followup_date"),
        detector.get("message"),
        detector.get("date")
    ))
    conn.commit()
    conn.close()

def save_life_event(detector):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO life_events (emotion, concern, state, resolved, severity,
        event_worthy, is_future_event, followup_date, message, date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        detector.get("emotion"),
        detector.get("concern"),
        detector.get("state"),
        1 if detector.get("resolved") else 0,
        detector.get("severity"),
        1 if detector.get("event_worthy") else 0,
        1 if detector.get("is_future_event") else 0,
        detector.get("followup_date"),
        detector.get("message"),
        detector.get("date")
    ))
    conn.commit()
    conn.close()

def get_active_concerns(user_id):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT concern FROM concerns
        WHERE resolved = 0 
        AND severity IN ('medium', 'high')
        AND user_id = ?
    """, (user_id,))
    results = cursor.fetchall()
    conn.close()
    return [r[0] for r in results if r[0]]

def get_recent_life_events(user_id):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT message FROM life_events
        WHERE message IS NOT NULL 
        AND date >= ?
        AND user_id = ?
        ORDER BY id DESC LIMIT 10
    """, (cutoff, user_id))
    results = cursor.fetchall()
    conn.close()
    return [r[0] for r in results]

def get_followups(user_id):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT message FROM life_events
        WHERE followup_date IS NOT NULL 
        AND followup_date <= ?
        AND resolved = 0
        AND message IS NOT NULL
        AND user_id = ?
    """, (today, user_id))
    results = cursor.fetchall()
    conn.close()
    return [r[0] for r in results]

def mark_resolved(concern_text):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE concerns SET resolved = 1
        WHERE concern = ?
    """, (concern_text,))
    cursor.execute("""
        UPDATE life_events SET resolved = 1
        WHERE resolved = 0
    """)
    conn.commit()
    conn.close()

import sqlite3
conn = sqlite3.connect("heim.db")
cursor = conn.cursor()
cursor.execute("SELECT concern, severity, resolved FROM concerns ORDER BY id DESC LIMIT 10")
print(cursor.fetchall())
conn.close()

def save_conversation_summary(conversation_id, summary):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE conversations SET summary = ? WHERE id = ?
    """, (summary, conversation_id))
    conn.commit()
    conn.close()

def save_conversation_summary(conversation_id, summary):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE conversations SET summary = ? WHERE id = ?
    """, (summary, conversation_id))
    conn.commit()
    conn.close()

def get_conversation_summaries():
    def get_conversations(user_id):
        conn = sqlite3.connect("heim.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title FROM conversations
            WHERE user_id = ?
            ORDER BY last_updated DESC
        """, (user_id,))
        conversations = cursor.fetchall()
        conn.close()
        return conversations

def create_user(username, password):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, created_at)
            VALUES (?, ?, datetime('now'))
        """, (username, password))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None  # username already exists

def get_user(username, password):
    conn = sqlite3.connect("heim.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, username FROM users 
        WHERE username = ? AND password = ?
    """, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

if __name__ == "__main__":
    init_db()
    print("database created")
