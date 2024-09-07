# voice_interface.py
#import speech_recognition as sr
#import pyttsx3

#def speak(text):
    # Initialize the text-to-speech engine
   # engine = pyttsx3.init()
   # engine.say(text)
   # engine.runAndWait()

#def listen():
    # Initialize the recognizer
   # recognizer = sr.Recognizer()
   # with sr.Microphone() as source:
       # print("Listening...")
       # recognizer.adjust_for_ambient_noise(source)
       # audio = recognizer.listen(source)

       # try:
           # command = recognizer.recognize_google(audio)
           # print(f"Recognized: {command}")
           # return command
       # except sr.UnknownValueError:
           # print("Sorry, I did not understand that.")
           # return None
       # except sr.RequestError:
         #   print("Could not request results; check your network connection.")
          #  return None



# voice_interface.py
import speech_recognition as sr
import pyttsx3
import queue

command_queue = queue.Queue()  # Global command queue

def speak(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

def listen_for_commands():
    """Continuously listen for commands and add them to the queue."""
    while True:
        command = listen()
        if command:
            command_queue.put(command)
