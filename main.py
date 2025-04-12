import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
from Information import infow
from Yt import youtubeVideo
from AppAnalyzer import AppReviewAnalyzer
import re

def clean_text(text):
    """Clean text by keeping only alphanumeric characters, spaces, commas, and periods."""
    cleaned_text = re.sub(r'[^\w\s,.]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    """Speak out the given text."""
    engine.say(text)
    engine.runAndWait()

# Configure Generative AI
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(model_name='gemini-1.5-flash')
convo = model.start_chat(history=[
    {"role": "user", "parts": ["How wifi works"]},
    {"role": "model", "parts": ["... (Generated response as per your previous conversation) ..."]},
])

# Initialize Speech Recognition

def listen_once():
    """Listen for a single voice command."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.write("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1.2)
            st.write("Listening...")
            audio = recognizer.listen(source, timeout=5)
            try:
                command = recognizer.recognize_google(audio)
                return command
            except sr.UnknownValueError:
                st.warning("Could not understand audio")
            except sr.RequestError as e:
                st.error(f"Recognition error: {e}")
    except Exception as e:
        st.error(f"Microphone error: {e}")
    return None

# Streamlit App
def main():
    st.title("Phoenix Voice Assistant")
    st.write("Hello there, I am your voice assistant. My name is Phoenix.")
    speak("Hello there, I am your voice assistant. My name is Phoenix.")
    i = 0
    while i != 10:
        st.write("Listening... Say 'exit' to stop.")
        command = listen_once()
        if command:
            st.write(f"You said: {command}")
            if "exit" in command.lower():
                speak("Exiting listening mode.")
            else:
                process_command(command)
        i += 1

def process_command(command):
    """Process recognized voice commands."""
    if "information" in command.lower():
        speak("Please specify the topic you want information about.")
        topic = listen_once()
        if topic:
            st.write(f"Searching for {topic} on Wikipedia...")
            assist = infow()
            result = assist.get_info(topic)
            # st.write(result)
            # speak(result[:200])  # Speak the first 200 characters

    elif "play" in command.lower() and "youtube" in command.lower():
        speak("What video do you want to play?")
        video_name = listen_once()
        if video_name:
            st.write(f"Searching for {video_name} on YouTube...")
            assist = youtubeVideo()
            result = assist.get_info(video_name)
            st.write(result)
            speak(f"Playing {video_name} on YouTube.")

    elif "suggest" in command.lower() and "apps" in command.lower():
        speak("Please specify the category of apps.")
        category = listen_once()
        if category:
            st.write(f"Analyzing apps in the {category} category...")
            analyzer = AppReviewAnalyzer()
            analysis_df = analyzer.analyze_apps(category)
            best_app = analyzer.suggest_best_app(analysis_df)
            st.write(f"The best app in the {category} category is {best_app['app_name']}.")
            speak(f"The best app in the {category} category is {best_app['app_name']}.")

    else:
        speak("What question do you have?")
        response = convo.send_message(command)
        cleaned_response = clean_text(response.text)
        st.write(cleaned_response)
        speak(cleaned_response)

if __name__ == "__main__":
    main()
