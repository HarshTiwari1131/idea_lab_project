import tkinter as tk
from sensor_detection import detect_person
from voice_interface import speak, listen
from open_close import open_application, close_application, search_web
from openai_api import generate_chat_response
from movie_api import get_movie_details  # Import the movie API function
import datetime
import json
import os
from weather import get_weather_info
from news_api import news
from finance_api import get_stock_data  # Import the stock data function

def wish_me():
    """Function to greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your personal assistant. How can I help you today?")

def ask_questions():
    """Function to ask questions to the user and store responses."""
    try:
        with open('questions.json', 'r') as f:
            questions = json.load(f)
    except FileNotFoundError:
        speak("The questions file is missing.")
        return
    except json.JSONDecodeError:
        speak("The questions file is not in the correct format.")
        return

    responses = {}
    for question in questions:
        speak(question)
        response = listen()
        if response:
            responses[question] = response
        else:
            responses[question] = "No response detected."

    with open('responses.json', 'w') as f:
        json.dump(responses, f, indent=4)
    
    speak("Thank you for your responses. They have been recorded.")

def handle_openai_command(command):
    """Use OpenAI API to handle unknown commands."""
    messages = [{"role": "user", "content": command}]
    response = generate_chat_response(messages)
    if response:
        speak(response)
    else:
        speak("I'm unable to process your request right now.")

def handle_movie_command(command):
    """Handle commands related to fetching movie details."""
    movie_name = command.split("movie", 1)[1].strip()
    movie_details = get_movie_details(movie_name)
    
    if isinstance(movie_details, dict):
        speak(f"Title: {movie_details['title']}")
        speak(f"Release Date: {movie_details['release_date']}")
        speak(f"Overview: {movie_details['overview']}")
        speak(f"Rating: {movie_details['vote_average']} out of 10")
    else:
        speak(movie_details)



def handle_stock_command(command):
    """Handle commands related to fetching stock details."""
    symbol = command.split("stock", 1)[1].strip()
    speak(f"Fetching data for {symbol} stock.")
    try:
        # Get stock data (default interval is 1 minute)
        get_stock_data(symbol)
    except Exception as e:
        speak(f"Error fetching stock data: {str(e)}")



def main_loop():
    """Main loop for processing voice commands."""
    wish_me()
    
    while True:
        command = listen()

        if command:
            command = command.lower()

            if "open" in command:
                app_name = command.split("open", 1)[1].strip()
                open_application(app_name)
                speak(f"Opening {app_name}")

            elif "close" in command:
                app_name = command.split("close", 1)[1].strip()
                close_application(app_name)
                speak(f"Closing {app_name}")

            elif "search" in command:
                query = command.split("search", 1)[1].strip()
                search_web()  # Include query in search_web function
                speak(f"Searching for {query}")

            elif "ask questions" in command:
                ask_questions()

            elif "weather" in command:
                weather_info = get_weather_info()
                speak(f"The temperature is {weather_info['temp']} degrees Celsius with {weather_info['description']}.")

            elif "news" in command:
                headlines = news()
                speak("Here are the top news headlines.")
                for headline in headlines:
                    speak(headline)
            
            elif "movie" in command:
                handle_movie_command(command)


            elif "stock" in command:
                handle_stock_command(command)

            elif "quit" in command or "exit" in command:
                speak("Goodbye! Have a nice day.")
                break


            else:
                handle_openai_command(command)  # Use OpenAI API for unknown commands

if __name__ == "__main__":
    detect_person()  # Start person detection
    main_loop()  # Start the main loop


# import tkinter as tk
# from sensor_detection import detect_person
# from voice_interface import speak, listen, listen_for_commands, command_queue
# from open_close import open_application, close_application, search_web
# import datetime
# import json
# import os
# from weather import *
# from news import *
# import threading
# import time

# def wish_me():
#     """Function to greet the user based on the time of day."""
#     hour = datetime.datetime.now().hour
#     if 0 <= hour < 12:
#         speak("Good Morning!")
#     elif 12 <= hour < 18:
#         speak("Good Afternoon!")
#     else:
#         speak("Good Evening!")
#     speak("I am your personal assistant. How can I help you today?")

# def ask_questions():
#     """Function to ask questions to the user and store responses."""
#     try:
#         with open('questions.json', 'r') as f:
#             questions = json.load(f)
#     except FileNotFoundError:
#         speak("The questions file is missing.")
#         return
#     except json.JSONDecodeError:
#         speak("The questions file is not in the correct format.")
#         return

#     responses = {}
#     for question in questions:
#         speak(question)
#         response = listen()
#         if response:
#             responses[question] = response
#         else:
#             responses[question] = "No response detected."

#     with open('responses.json', 'w') as f:
#         json.dump(responses, f, indent=4)
    
#     speak("Thank you for your responses. They have been recorded.")

# def process_command(command):
#     """Process a single command."""
#     if "open" in command:
#         app_name = command.split("open", 1)[1].strip()
#         open_application(app_name)
#         speak(f"Opening {app_name}")

#     elif "close" in command:
#         app_name = command.split("close", 1)[1].strip()
#         close_application(app_name)
#         speak(f"Closing {app_name}")

#     elif "search" in command:
#         query = command.split("search", 1)[1].strip()
#         search_web()  # Corrected the argument to include the query
#         speak(f"Searching for {query}")

#     elif "ask questions" in command:
#         ask_questions()

#     elif "news" in command:
#         headlines = news()
#         for headline in headlines:
#             speak(headline)
    
#     elif "quit" in command or "exit" in command:
#         speak("Goodbye! Have a nice day.")
#         return False

#     else:
#         speak("I'm sorry, I didn't understand that command.")
#     return True

# def main_loop():
#     """Main loop for processing voice commands."""
#     wish_me()
    
#     # Start listening in a separate thread
#     listening_thread = threading.Thread(target=listen_for_commands)
#     listening_thread.daemon = True
#     listening_thread.start()

#     while True:
#         if not command_queue.empty():
#             command = command_queue.get()
#             print(f"Processing command: {command}")  # Debugging print
#             if not process_command(command):
#                 break
#         time.sleep(0.1)  # To avoid tight loop, adding a small delay

# if __name__ == "__main__":
#     detect_person()  # Start person detection
#     main_loop()  # Start the main loop



# import tkinter as tk
# from sensor_detection import detect_person
# from voice_interface import speak, listen, listen_for_commands, command_queue
# from open_close import open_application, close_application, search_web
# from openai_api import generate_chat_response
# import datetime
# import json
# import os
# from weather import get_weather_info
# from news import news
# import threading
# import time

# def wish_me():
#     """Function to greet the user based on the time of day."""
#     hour = datetime.datetime.now().hour
#     if 0 <= hour < 12:
#         speak("Good Morning!")
#     elif 12 <= hour < 18:
#         speak("Good Afternoon!")
#     else:
#         speak("Good Evening!")
#     speak("I am your personal assistant. How can I help you today?")

# def ask_questions():
#     """Function to ask questions to the user and store responses."""
#     try:
#         with open('questions.json', 'r') as f:
#             questions = json.load(f)
#     except FileNotFoundError:
#         speak("The questions file is missing.")
#         return
#     except json.JSONDecodeError:
#         speak("The questions file is not in the correct format.")
#         return

#     responses = {}
#     for question in questions:
#         speak(question)
#         response = listen()
#         if response:
#             responses[question] = response
#         else:
#             responses[question] = "No response detected."

#     with open('responses.json', 'w') as f:
#         json.dump(responses, f, indent=4)
    
#     speak("Thank you for your responses. They have been recorded.")

# def process_command(command):
#     """Process a single command."""
#     if "open" in command:
#         app_name = command.split("open", 1)[1].strip()
#         open_application(app_name)
#         speak(f"Opening {app_name}")

#     elif "close" in command:
#         app_name = command.split("close", 1)[1].strip()
#         close_application(app_name)
#         speak(f"Closing {app_name}")

#     elif "search" in command:
#         query = command.split("search", 1)[1].strip()
#         search_web()  # Corrected the argument to include the query
#         speak(f"Searching for {query}")

#     elif "ask questions" in command:
#         ask_questions()

#     elif "news" in command:
#         headlines = news()
#         for headline in headlines:
#             speak(headline)
    
#     elif "weather" in command:
#         weather_info = get_weather_info()
#         speak(f"The temperature is {weather_info['temp']} degrees Celsius and the weather is {weather_info['description']}.")

#     elif "chat" in command:
#         query = command.split("chat", 1)[1].strip()
#         response = generate_chat_response([{"role": "user", "content": query}])
#         if response:
#             speak(response)
    
#     elif "quit" in command or "exit" in command:
#         speak("Goodbye! Have a nice day.")
#         return False

#     else:
#         speak("I'm sorry, I didn't understand that command.")
#     return True

# def main_loop():
#     """Main loop for processing voice commands."""
#     wish_me()
    
#     # Start listening in a separate thread
#     listening_thread = threading.Thread(target=listen_for_commands)
#     listening_thread.daemon = True
#     listening_thread.start()

#     while True:
#         if not command_queue.empty():
#             command = command_queue.get()
#             print(f"Processing command: {command}")  # Debugging print
#             if not process_command(command):
#                 break
#         time.sleep(0.1)  # To avoid tight loop, adding a small delay

# if __name__ == "__main__":
#     detect_person()  # Start person detection
#     main_loop()  # Start the main loop
