from flask import Flask, request, jsonify, render_template
from emotion_ai2 import get_reply

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    print("received:", user_message)  # add this
    reply = get_reply(user_message)
    print("reply:", reply)  # add this
    return jsonify({"reply": reply})



if __name__ == "__main__":
    app.run(debug=True)