# version 0.2 - AI powered emotion and concern detection
# replaces manual keyword matching with actual AI understanding
# automatically detects emotion, concern, state from natural language
# saves everything to concern.json permanently
# next step: response layer - AI talks back like a friend
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
system_prompt = "when a user sends you a message, analyze for hidden emotions, don't overcomplicate, respond only in JSON with three fields: emotion, concern, state"
user_message = input("talk to me: ")
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
)

print(response.choices[0].message.content)
detector = json.loads(response.choices[0].message.content)
with open("concern.json", "r") as f:
    concern = json.load(f)

concern.append(detector)

with open("concern.json", "w") as f:
    json.dump(concern, f)