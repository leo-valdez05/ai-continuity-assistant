import os
from flask import Flask, request, jsonify, render_template
from database import init_db, create_conversation, save_message, get_conversations,update_conversation_title

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

    reply, emotion, floor_color,leaving = get_reply(user_message)


    if conversation_id:
        save_message(conversation_id, "user", user_message)
        save_message(conversation_id, "ai", reply)
        update_conversation_title(conversation_id, user_message[:50])

        return jsonify({"reply": reply, "emotion": emotion, "floor_color": floor_color, "leaving": leaving})

@app.route("/messages/<int:conv_id>")
def show_messages(conv_id):
    from database import get_messages
    return jsonify(get_messages(conv_id))

@app.route("/conversations")
def conversations():
    from database import get_conversations
    return jsonify(get_conversations())


@app.route("/end_conversation", methods=["POST"])
def end_conversation():
    data = request.json
    conversation_id = data.get("conversation_id")
    messages = data.get("messages")

    if not conversation_id or not messages:
        return jsonify({"status": "ok"})

    import anthropic
    ai = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    summary_response = ai.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        system="Generate a short 5-7 word title summarizing this conversation. Return ONLY the title, nothing else. No quotes, no punctuation at the end.",
        messages=[{"role": "user", "content": str(messages)}]
    )

    title = summary_response.content[0].text.strip()

    from database import save_conversation_summary, update_conversation_title
    save_conversation_summary(conversation_id, title)
    update_conversation_title(conversation_id, title)

    return jsonify({"status": "ok", "title": title})

if __name__ == "__main__":
    app.run(debug=True)
