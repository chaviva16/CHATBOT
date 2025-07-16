# ---------- intent_detector.py ----------
def get_intent(user_input):
    keywords = {
        "greeting": ["hello", "hi", "hey"],
        "farewell": ["bye", "goodbye", "see you"],
        "thanks": ["thank", "thanks"],
        "date": ["date", "today"],
        "time": ["time", "clock"],
        "math": ["add", "subtract", "multiply", "divide"],
        "weather": ["weather", "temperature", "forecast"],
        "news": ["news", "headlines"],
        "jokes": ["joke", "funny"],
        "conversion": ["convert", "conversion"],
        "fun facts": ["fact", "fun", "interesting"]
    }
    for intent, words in keywords.items():
        if any(word in user_input.lower() for word in words):
            return intent
    return "unknown"