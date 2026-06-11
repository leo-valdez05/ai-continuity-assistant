from flask import Flask, request, jsonify, render_template
from database import init_db, create_conversation, save_message, get_conversations
from emotion_ai2 import get_reply

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/new_conversation", methods=["POST"])
def new_conversation():
    data = request.json
    title = data.get("title", "New Chat")
    conv_id = create_conversation(title)
    return jsonify({"conversation_id": conv_id})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    conversation_id = data.get("conversation_id")

    print("conversation_id received:", conversation_id)

    reply, emotion, floor_color = get_reply(user_message)

    if conversation_id:
        save_message(conversation_id, "user", user_message)
        save_message(conversation_id, "ai", reply)

    return jsonify({"reply": reply, "emotion": emotion, "floor_color": floor_color})

@app.route("/messages/<int:conv_id>")
def show_messages(conv_id):
    from database import get_messages
    return jsonify(get_messages(conv_id))

@app.route("/conversations")
def conversations():
    from database import get_conversations
    return jsonify(get_conversations())

if __name__ == "__main__":
    app.run(debug=True)
