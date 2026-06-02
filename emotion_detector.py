# version 0.1 - basic emotion detection using keyword matching
# limitation: manual keywords, won't catch everything
# next step: replace with AI based detection in version 0.4
emotions = {
    "stress": [
        "i am overwhelmed",
        "i have too much work",
        "i don't know what to do",
        "everything is piling up",
        "i feel exhausted",
        "i am struggling",
        "this is difficult"
    ],
    "anxiety": [
        "i am worried",
        "what if it goes wrong",
        "i am nervous",
        "i can't stop thinking about it",
        "i am scared",
        "i feel uncertain"
    ],
    "sadness": [
        "i feel alone",
        "i miss them",
        "nothing feels right",
        "i feel empty",
        "i am disappointed"
    ],
    "excitement": [
        "i got selected",
        "i am so happy",
        "i did it",
        "this is amazing",
        "i achieved my goal"
    ]
}
user_feeling = input("enter your words: ").lower()

for emotion, keywords in emotions.items():
    for keyword in keywords:
        if keyword in user_feeling:
            print(emotion , "detected")
