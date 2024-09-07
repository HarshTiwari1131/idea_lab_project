import os
import subprocess
import webbrowser
from voice_interface import speak, listen
import wikipedia
from urllib.parse import quote
import pafy
import yt_dlp


def open_application(app_name):
    # Open common applications using their executable name
    try:
        if app_name.lower() == "notepad":
            os.system("notepad")
        elif app_name.lower() == "calculator":
            subprocess.Popen("calc.exe")
        elif app_name.lower() == "paint":
            os.system("mspaint")
        elif app_name.lower() == "wordpad":
            os.system("write")
        elif app_name.lower() == "vlc":
            subprocess.Popen(r'"C:\Program Files\VideoLAN\VLC\vlc.exe"')
        elif app_name.lower() == "microsoft store":
            subprocess.Popen("start ms-windows-store:", shell=True)
        elif app_name.lower() == "file explorer":
            os.system("explorer")
        elif app_name.lower() == "microsoft word":
            subprocess.Popen(r'"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"')
        elif app_name.lower() == "microsoft excel":
            subprocess.Popen(r'"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"')
        elif app_name.lower() == "adobe photoshop":
            subprocess.Popen(r'"C:\Program Files\Adobe\Adobe Photoshop 2023\Photoshop.exe"')
        elif app_name.lower() == "adobe illustrator":
            subprocess.Popen(r'"C:\Program Files\Adobe\Adobe Illustrator 2023\Support Files\Contents\Windows\Illustrator.exe"')
        else:
            print(f"Application {app_name} is not configured to be opened.")
    except Exception as e:
        print(f"Error opening application: {e}")

def close_application(app_name):
    try:
        if app_name.lower() == "notepad":
            os.system("taskkill /f /im notepad.exe")
        elif app_name.lower() == "calculator":
            os.system("taskkill /f /im calculator.exe")
        elif app_name.lower() == "paint":
            os.system("taskkill /f /im mspaint.exe")
        elif app_name.lower() == "wordpad":
            os.system("taskkill /f /im wordpad.exe")
        elif app_name.lower() == "vlc":
            os.system("taskkill /f /im vlc.exe")
        elif app_name.lower() == "microsoft word":
            os.system("taskkill /f /im WINWORD.EXE")
        elif app_name.lower() == "microsoft excel":
            os.system("taskkill /f /im EXCEL.EXE")
        elif app_name.lower() == "adobe photoshop":
            os.system("taskkill /f /im Photoshop.exe")
        elif app_name.lower() == "adobe illustrator":
            os.system("taskkill /f /im Illustrator.exe")
        else:
            print(f"Application {app_name} is not configured to be closed.")
    except Exception as e:
        print(f"Error closing application: {e}")


def get_first_youtube_url(query):
    """Fetch the URL of the first YouTube video based on the query."""
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Use yt-dlp to get search results
            result = ydl.extract_info(f"ytsearch:{query}", download=False)
            if 'entries' in result and len(result['entries']) > 0:
                first_video = result['entries'][0]
                return first_video['webpage_url']
            else:
                return None
        except Exception as e:
            print(f"Error fetching YouTube video URL: {e}")
            return None

def search_web():
    # Ask user what to search
    speak("What would you like to search?")
    query = listen().lower().strip()  # Convert the query to lowercase and strip any extra whitespace

    if not query:
        speak("I didn't hear anything. Please try again.")
        return

    # Check which platform the user wants to search on
    if 'google' in query:
        query = query.replace('google', '').strip()  # Remove 'google' from query
        webbrowser.open(f"https://www.google.com/search?q={quote(query)}")  # Google
    elif 'wikipedia' in query:
        query = query.replace('wikipedia', '').strip()  # Remove 'wikipedia' from query
        speak('Searching Wikipedia...')
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("The term you searched for is ambiguous. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any results on Wikipedia.")
    elif 'duckduckgo' in query:
        query = query.replace('duckduckgo', '').strip()  # Remove 'duckduckgo' from query
        webbrowser.open(f"https://duckduckgo.com/?q={quote(query)}")  # DuckDuckGo
    elif 'yahoo' in query:
        query = query.replace('yahoo', '').strip()  # Remove 'yahoo' from query
        webbrowser.open(f"https://search.yahoo.com/search?p={quote(query)}")  # Yahoo
    elif 'youtube' in query:
        query = query.replace('youtube', '').strip()  # Remove 'youtube' from query
        if query:  # If the user provided a query after 'youtube'
            speak(f"Searching YouTube for {query}...")
            youtube_url = get_first_youtube_url(query)
            if youtube_url:
                webbrowser.open(youtube_url)  # Open the first YouTube video in the default web browser
                speak("Playing the first video result from YouTube.")
            else:
                speak("Sorry, I couldn't find any video on YouTube.")
        else:
            speak("Please specify what to search on YouTube.")
    else:
        webbrowser.open(f"https://www.bing.com/search?q={quote(query)}")  # Bing

    speak("Here are the search results.")


