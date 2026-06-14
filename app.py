import os
from flask import Flask, request, jsonify, render_template,session, redirect, url_for
from database import init_db, create_conversation, save_message, get_conversations,update_conversation_title, create_user, get_user

from emotion_ai2 import get_reply,reset_chat_history, get_chat_history, update_profile

app = Flask(__name__)
app.secret_key = "heim_secret_key_change_this_later"
init_db()

@app.route("/")
def home():
    if "user_id" not in session:
        return render_template("login.html")
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user_id = create_user(username, password)
    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        return jsonify({"success": True, "username": username})
    else:
        return jsonify({"success": False, "error": "Username already taken"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = get_user(username, password)
    if user:
        session["user_id"] = user[0]
        session["username"] = user[1]
        return jsonify({"success": True, "username": user[1]})
    else:
        return jsonify({"success": False, "error": "Wrong username or password"})

@app.route("/logout", methods=["POST"])
def logout():
    from emotion_ai2 import reset_chat_history
    reset_chat_history()
    session.clear()
    return jsonify({"success": True})

@app.route("/me")
def me():
    if "user_id" in session:
        return jsonify({"logged_in": True, "username": session["username"]})
    return jsonify({"logged_in": False})

@app.route("/new_conversation", methods=["POST"])
def new_conversation():
    data = request.json
    title = data.get("title", "New Chat")
    conv_id = create_conversation(title, session.get("user_id"))
    return jsonify({"conversation_id": conv_id})

@app.route("/conversations")
def conversations():
    return jsonify(get_conversations(session.get("user_id")))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    conversation_id = data.get("conversation_id")

    print("conversation_id received:", conversation_id)

    reply, emotion, floor_color,leaving = get_reply(user_message,session.get("user_id"))


    if conversation_id:
        save_message(conversation_id, "user", user_message)
        save_message(conversation_id, "ai", reply)
        update_conversation_title(conversation_id, user_message[:50])

        return jsonify({"reply": reply, "emotion": emotion, "floor_color": floor_color, "leaving": leaving})

@app.route("/messages/<int:conv_id>")
def show_messages(conv_id):
    from database import get_messages
    return jsonify(get_messages(conv_id))


@app.route("/end_conversation", methods=["POST"])
def end_conversation():
    from database import save_conversation_summary, update_conversation_title
    from emotion_ai2 import update_profile, get_chat_history

    data = request.json
    conversation_id = data.get("conversation_id")
    messages = data.get("messages")

    if not conversation_id or not messages:
        return jsonify({"status": "ok"})

    user_id = session.get("user_id")

    if user_id:
        update_profile(user_id, get_chat_history())

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
