import pyttsx3 as p
import speech_recognition as sr
import google.generativeai as genai
from Information import infow
from YT import youtubeVideo
from AppAnalyzer import AppReviewAnalyzer
import re

def clean_text(text):

    # Keep only alphanumeric characters, spaces, commas, and periods
    cleaned_text = re.sub(r'[^\w\s,.]', '', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text


engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# print(voices)

def speak(text):
    engine.say(text)
    engine.runAndWait()


r = sr.Recognizer()
speak("hello there I am ur voice assistant. My name is phoenix")

with sr.Microphone() as source:
    r.energy_threshold = 10000
    r.adjust_for_ambient_noise(source, 1.2)
    speak("How are you sir?")
    print("Listening....")

    audio = r.listen(source)
    text = r.recognize_google(audio)
    print(text)

if "what about you" in text:
    speak("I am also having a good day sir")
speak("What can I do for You?")


#GEMINI API WORKS
genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel(model_name='gemini-1.5-flash')

convo = model.start_chat(history=[
    {"role": "user", "parts": ["How wifi works"]},
    {"role": "model", "parts": ["... (Generated response as per your previous conversation) ..."]},
])

i=0
while(i!=10):
    i+=1
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise(source, 1.2)
        # speak("How are you sir?")
        print("Listening....")

        audio = r.listen(source)
        text2 = r.recognize_google(audio)
        print(text2) #Can you get me some information?
        text2 = text2.lower()

    if "information" in text2:
        speak("Please specify what is the topic")
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("Listening....")

            audio = r.listen(source)
            inform = r.recognize_google(audio)
            print(inform)
        speak("Searching for {} on wikipedia".format(inform))
        assist = infow()
        assist.get_info(inform)



    elif "play" in text2 and "youtube" in text2:
        speak("What you want to watch?")
        print("Listening....")
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("Listening....")

            audio = r.listen(source)
            resp = r.recognize_google(audio)
            print(resp)
        # speak("Searching for {} on wikipedia".format(inform))
        assist = youtubeVideo()
        assist.get_info(resp)
    elif "apps" in text2 and "suggest " in text2:
        speak("Please specify the category of apps.")
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("Listening....")
            audio = r.listen(source)
            category = r.recognize_google(audio)
        analyzer = AppReviewAnalyzer()
        speak(f"Analyzing apps in the {category} category")
        analysis_df = analyzer.analyze_apps(category)
        best_app = analyzer.suggest_best_app(analysis_df)
        speak(f"The best app in the {category} category is {best_app['app_name']}")
        analysis_df.to_csv(f"Review_Analysis_{category}.csv", index=False)
        print(f"Review analysis for {category} saved to CSV.")
    elif "exit" in text2 or "thank you" in text2:
        speak("Thank you sir, Bye untill next time")
        break
    # elif "generate" in text2 or "tell me" in text2:
    else:
        speak("Please specify what is the topic")
        with sr.Microphone() as source:
            r.energy_threshold = 10000
            r.adjust_for_ambient_noise(source, 1.2)
            print("Listening....")

            audio = r.listen(source)
            para = r.recognize_google(audio)
            print(para)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 140)
        response = convo.send_message(para)
        cleaned_response = clean_text(response.text)
        print(cleaned_response)
        speak(cleaned_response)