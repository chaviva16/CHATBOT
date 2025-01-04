import datetime
import random
import re
import requests
import sched
import time
from datetime import timedelta
import threading

import winsound  # For audio alert on Windows

# Initialize the scheduler
scheduler = sched.scheduler(time.time, time.sleep)

# Step 1: Define intents and responses
responses = {
    "greeting": ["Hello! How can I assist you today?", "Hi there! What can I do for you?", "Hey! Need any help?"],
    "farewell": ["Goodbye! Have a great day!", "See you later!", "Bye! Take care!"],
    "thanks": ["You're welcome!", "No problem!", "Happy to help!"],
    "date": ["Today's date is {date}.", "It's {date} today."],
    "time": ["The current time is {time}.", "It's {time} now."],
    "math": ["The result is {result}.", "That equals {result}."],
    "weather": ["The weather in {city} is currently {description} with a temperature of {temp}°C.", "In {city}, it's {description} and {temp}°C."],
    "news": ["Here are the top news headlines:\n{headlines}", "Today's headlines are:\n{headlines}"],
    "unknown": ["I'm sorry, I don't understand that.", "Could you rephrase?", "I'm not sure how to help with that."],
    "jokes": ["Why don't scientists trust atoms? Because they make up everything!", 
              "Why did the scarecrow win an award? Because he was outstanding in his field!",
              "Why don't programmers like nature? It has too many bugs."],
    "conversion": ["{value} {from_unit} is equal to {converted_value} {to_unit}.", 
                   "The conversion of {value} {from_unit} is {converted_value} {to_unit}."],
    
    "fun facts": ["Did you know? {fact}", "Here's a fun fact: {fact}"],
    "reminder": ["Reminder set for {time}.", "I'll remind you at {time}."],
    "alarm": ["Alarm set for {time}.", "I'll alarm you at {time}."]
}

# Step 2: Define a function to handle intents
def get_intent(user_input):
    # Define keywords for each intent
    keywords = {
        "greeting": ["hello", "hi", "hey"],
        "farewell": ["bye", "goodbye", "see you"],
        "thanks": ["thank", "thanks"],
        "date": ["date", "today"],
        "time": ["time", "clock"],
        "math": ["add", "subtract", "multiply", "divide"],
        "weather": ["weather", "temperature", "forecast"],
        "news": ["news", "headlines", "updates"],
        "jokes": ["joke", "funny", "laugh"],
        "conversion": ["convert", "conversion"],
        
        "fun facts": ["fact", "fun", "interesting"],
        "reminder": ["remind", "reminder"],
        "alarm": ["alarm", "set alarm"]
    }
    
    # Match user input with keywords
    for intent, words in keywords.items():
        if any(word in user_input.lower() for word in words):
            return intent
    return "unknown"

# Step 3: Define a function to perform tasks based on the intent
def perform_task(intent, user_input):
    if intent == "greeting":
        return random.choice(responses["greeting"])
    elif intent == "farewell":
        return random.choice(responses["farewell"])
    elif intent == "thanks":
        return random.choice(responses["thanks"])
    elif intent == "date":
        current_date = datetime.date.today().strftime("%B %d, %Y")
        return random.choice(responses["date"]).format(date=current_date)
    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return random.choice(responses["time"]).format(time=current_time)
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
        return handle_fun_facts(user_input)
    elif intent == "reminder":
        return handle_reminder(user_input)
    elif intent == "alarm":
        return handle_alarm(user_input)
    else:
        return random.choice(responses["unknown"])

# Step 4: Define a function to handle math operations
def handle_math(user_input):
    match = re.search(r"(\d+)\s*(add|subtract|multiply|divide)\s*(\d+)", user_input.lower())
    if match:
        num1 = int(match.group(1))
        operation = match.group(2)
        num2 = int(match.group(3))
        
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            result = num1 / num2 if num2 != 0 else "undefined (division by zero)"
        else:
            result = "unknown operation"
        
        return random.choice(responses["math"]).format(result=result)
    else:
        return "I couldn't understand the math problem."

# Step 5: Define a function to fetch weather information
def get_weather(user_input):
    api_key = "20267473154b66c769fcdf54db00cc95"  # Replace with your OpenWeatherMap API key
    city_match = re.search(r"weather in (\w+)", user_input.lower())
    if city_match:
        city = city_match.group(1)
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            if data["cod"] == 200:
                description = data["weather"][0]["description"]
                temp = data["main"]["temp"]
                return random.choice(responses["weather"]).format(city=city, description=description, temp=temp)
            else:
                return f"Sorry, I couldn't find weather information for {city}."
        except requests.exceptions.RequestException as e:
            return f"There was an error fetching the weather information: {e}"
    else:
        return "Please specify a city for the weather, like 'What's the weather in Lagos?'"

# Step 6: Define a function to fetch news headlines
def get_news():
    api_key = "063611b390d0479d8fb007c8492ed191"  # Replace with your News API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        if data["status"] == "ok":
            headlines = "\n".join([article["title"] for article in data["articles"][:5]])
            return random.choice(responses["news"]).format(headlines=headlines)
        else:
            return "Sorry, I couldn't fetch the news at the moment."
    except requests.exceptions.RequestException as e:
        return f"There was an error fetching the news: {e}"

# Step 7: Define a function to handle unit conversion
def handle_conversion(user_input):
    match = re.search(r"(\d+)\s*(kilometers|km|miles|mi|kilograms|kg|pounds|lbs)\s*to\s*(kilometers|km|miles|mi|kilograms|kg|pounds|lbs)", user_input.lower())
    if match:
        value = float(match.group(1))
        from_unit = match.group(2)
        to_unit = match.group(4)
        
        if from_unit in ["kilometers", "km"] and to_unit in ["miles", "mi"]:
            converted_value = value * 0.621371
        elif from_unit in ["miles", "mi"] and to_unit in ["kilometers", "km"]:
            converted_value = value / 0.621371
        elif from_unit in ["kilograms", "kg"] and to_unit in ["pounds", "lbs"]:
            converted_value = value * 2.20462
        elif from_unit in ["pounds", "lbs"] and to_unit in ["kilograms", "kg"]:
            converted_value = value / 2.20462
        else:
            return "I cannot convert those units."

        return random.choice(responses["conversion"]).format(value=value, from_unit=from_unit, converted_value=converted_value, to_unit=to_unit)
    else:
        return "I couldn't understand the conversion request."



# Define a function to handle fun facts
def handle_fun_facts(user_input):
    facts = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "A day on Venus is longer than a year on Venus. It takes Venus about 243 Earth days to rotate once, but only about 225 Earth days to orbit the sun.",
        "Bananas are berries, but strawberries aren't.",
        "The Eiffel Tower can be 15 cm taller during the summer, due to the expansion of iron in the heat."
    ]
    fact = random.choice(facts)
    return random.choice(responses["fun facts"]).format(fact=fact)

# Define a function to handle reminders
def handle_reminder(user_input):
    match = re.search(r"remind me to (.+) at (\d+):(\d+)", user_input.lower())
    if match:
        task = match.group(1)
        hour = int(match.group(2))
        minute = int(match.group(3))
        
        now = datetime.datetime.now()
        reminder_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if reminder_time < now:
            reminder_time += timedelta(days=1)  # Schedule for the next day if the time has already passed
        
        delay = (reminder_time - now).total_seconds()
        scheduler.enter(delay, 1, print_reminder, argument=(task,))
        
        reminder_thread = threading.Thread(target=scheduler.run)
        reminder_thread.start()
        
        return random.choice(responses["reminder"]).format(time=reminder_time.strftime("%H:%M"))
    else:
        return "I couldn't understand the reminder request. Please use the format 'remind me to [task] at [HH:MM]'."

# Define a function to print the reminder
def print_reminder(task):
    print("Reminder: Don't forget to", task)

# Define a function to handle alarms
def handle_alarm(user_input):
    match = re.search(r"set an alarm for (\d+):(\d+)", user_input.lower())
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2))
        
        now = datetime.datetime.now()
        alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if alarm_time < now:
            alarm_time += timedelta(days=1)  # Schedule for the next day if the time has already passed
        
        delay = (alarm_time - now).total_seconds()
        scheduler.enter(delay, 1, play_alarm_sound)
        
        alarm_thread = threading.Thread(target=scheduler.run)
        alarm_thread.start()
        
        return random.choice(responses["alarm"]).format(time=alarm_time.strftime("%H:%M"))
    else:
        return "I couldn't understand the alarm request. Please use the format 'set an alarm for [HH:MM]'."

# Define a function to play the alarm sound
def play_alarm_sound():
    for _ in range(5):  # Beep 5 times
        winsound.Beep(1000, 1000)  # Frequency 1000 Hz, Duration 1000 ms

# Update perform_task function to handle the intents
def perform_task(intent, user_input):
    if intent == "greeting":
        return random.choice(responses["greeting"])
    elif intent == "farewell":
        return random.choice(responses["farewell"])
    elif intent == "thanks":
        return random.choice(responses["thanks"])
    elif intent == "date":
        current_date = datetime.date.today().strftime("%B %d, %Y")
        return random.choice(responses["date"]).format(date=current_date)
    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return random.choice(responses["time"]).format(time=current_time)
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
        return handle_fun_facts(user_input)
    elif intent == "reminder":
        return handle_reminder(user_input)
    elif intent == "alarm":
        return handle_alarm(user_input)
    else:
        return random.choice(responses["unknown"])

# Main chatbot loop
def chatbot():
    print("Chatbot: Hello! I'm your personal assistant chatbot. Type 'bye' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("Chatbot:", random.choice(responses["farewell"]))
            break
        intent = get_intent(user_input)
        response = perform_task(intent, user_input)
        print("Chatbot:", response)

# Run the chatbot
if __name__ == "__main__":
    chatbot()
 