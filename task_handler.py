import datetime
import random
import re
import requests

responses = {
    "greeting": ["Hello! ☺️", "Hi there! 👋", "Hey! Need help? 🤖"],
    "farewell": ["Goodbye! Take care! 👋", "See you later! 👀", "Bye for now! 💨"],
    "thanks": ["You're welcome! 🤗", "No problem at all! ☺️", "Glad to help! 🙌"],
    "date": ["Today's date is {date}. 🗕️"],
    "time": ["It's {time} now. ⏰"],
    "math": ["The result is {result}. 🔢"],
    "weather": ["Weather in {city}: {description}, {temp}°C 🌦️"],
    "news": ["Top headlines:\n{headlines} 🗞️"],
    "unknown": ["Hmm... I don't understand that 🤔", "Try asking in a different way! ❓"],
    "jokes": [
        "Why don't scientists trust atoms? Because they make up everything! 😂",
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🏆",
        "Why don't programmers like nature? It has too many bugs 🐞."
    ],
    "conversion": ["{value} {from_unit} is {converted_value:.2f} {to_unit}. 🔁"],
    "fun facts": ["Did you know? {fact} 🤯"]
}

def perform_task(intent, user_input):
    if intent == "greeting":
        return random.choice(responses["greeting"])
    elif intent == "farewell":
        return random.choice(responses["farewell"])
    elif intent == "thanks":
        return random.choice(responses["thanks"])
    elif intent == "date":
        date = datetime.date.today().strftime("%B %d, %Y")
        return responses["date"][0].format(date=date)
    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return responses["time"][0].format(time=current_time)
    elif intent == "math":
        return handle_math(user_input)
    elif intent == "weather":
        return get_weather(user_input)
    elif intent == "news":
        return get_news()
    elif intent == "jokes":
        return random.choice(responses["jokes"])
    elif intent == "conversion":
        return handle_conversion(user_input)
    elif intent == "fun facts":
        return handle_fun_facts()
    else:
        return random.choice(responses["unknown"])

def handle_math(user_input):
    match = re.search(r"(\d+)\s*(add|subtract|multiply|divide)\s*(\d+)", user_input.lower())
    if match:
        a, op, b = int(match.group(1)), match.group(2), int(match.group(3))
        result = {
            "add": a + b,
            "subtract": a - b,
            "multiply": a * b,
            "divide": a / b if b != 0 else "undefined"
        }.get(op, "unknown")
        return responses["math"][0].format(result=result)
    return "Try asking like '10 add 5' or '8 divide 2'"

def get_weather(user_input):
    api_key = "20267473154b66c769fcdf54db00cc95"
    match = re.search(r"weather in (\w+)", user_input.lower())
    if not match:
        return "Please specify a city like: 'weather in Lagos'."
    city = match.group(1)
    try:
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        ).json()
        desc = res["weather"][0]["description"]
        temp = res["main"]["temp"]
        return responses["weather"][0].format(city=city, description=desc, temp=temp)
    except:
        return "Couldn't get weather for that city."

def get_news():
    api_key = "063611b390d0479d8fb007c8492ed191"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        res = requests.get(url).json()
        if res["status"] == "ok":
            headlines = "\n".join([f"- {a['title']}" for a in res["articles"][:5]])
            return responses["news"][0].format(headlines=headlines)
        return "Couldn't fetch news 🗞️"
    except:
        return "Error while fetching news."

def handle_conversion(user_input):
    match = re.search(r"(\d+)\s*(km|mi|kg|lbs)\s*to\s*(km|mi|kg|lbs)", user_input.lower())
    if not match:
        return "Example: '10 km to mi' or '5 kg to lbs'"
    value = float(match.group(1))
    from_unit, to_unit = match.group(2), match.group(3)
    conversions = {
        ("km", "mi"): 0.621371, ("mi", "km"): 1.60934,
        ("kg", "lbs"): 2.20462, ("lbs", "kg"): 0.453592
    }
    key = (from_unit, to_unit)
    if key not in conversions:
        return "Conversion not supported."
    converted = value * conversions[key]
    return responses["conversion"][0].format(value=value, from_unit=from_unit, converted_value=converted, to_unit=to_unit)

def handle_fun_facts():
    facts = [
        "Bananas are berries, but strawberries aren't.",
        "Honey never spoils.",
        "Octopuses have three hearts.",
        "A day on Venus is longer than its year."
    ]
    return responses["fun facts"][0].format(fact=random.choice(facts))
