import json
# version 0.1 - basic concern storage
# user inputs a concern, gets saved to concerns.json permanently
# foundation of the continuity memory system


new_concern = {}
user_concern = input("what is your concern?")
user_feeling = input("what is your feeling?")
user_stage = input("is it done or still going on?")

new_concern["concern"] = user_concern
new_concern["feeling"] = user_feeling
new_concern["stage"] = user_stage
print(new_concern)
with open("concern.json", "r") as f:
    concern = json.load(f)

concern.append(new_concern)

with open("concern.json", "w") as f:
    json.dump(concern, f)