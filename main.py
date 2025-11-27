import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import openai
import os
import re

openai.api_key = "your-openai-api-key"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('rate', 175)

chat_history = ""

def say(text):
    print(f"D: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command(r=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        say("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        say("Recognizing...")
        query = r.recognize_google(audio)
        print(f"You said: {query}")
        return query.lower()
    except Exception as e:
        say("Sorry Boss, I couldn't understand that.")
        r

def ai_brain(prompt):
    global chat_history
    chat_history += f"Boss: {prompt}\nD: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chat_history,
        temperature=0.4,
        max_tokens=200
    )
    reply = response.choices[0].text.strip()
    chat_history += f"{reply}\n"
    say(reply)

def save_ai_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=200
    )
    result = response.choices[0].text.strip()
    filename = f"Openai/{re.sub(r'[^a-zA-Z0-9]', '_', prompt[:20])}.txt"
    os.makedirs("Openai", exist_ok=True)
    with open(filename, "w") as f:
        f.write(result)
    say("Saved your intelligent response, Boss.")

sites = {
     "instagram": "https://www.instagram.com/",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "wikipedia": "https://www.wikipedia.com"
}

if __name__ == "__main__":
    say("Hello Boss, I am D. Ready to assist you!")

    while True:
        query = take_command()

        if "exit" in query or "bye" in query:
            say("Alright Boss, see you soon!")
            break

        elif any(f"open {key}" in query for key in sites):
            for site in sites:
                if f"open {site}" in query:
                    say(f"Opening {site} for you, Boss.")
                    webbrowser.open(sites[site])
                    break

        elif "time" in query:
            time = datetime.datetime.now().strftime("%H:%M")
            say(f"Boss, the time is {time}")

        elif "chat with me" in query:
            say("Okay Boss, let's chat. Say 'exit' to stop.")
            while True:
                chat_input = take_command()
                if "exit" in chat_input:
                    say("Chat ended, Boss.")
                    break
                ai_brain(chat_input)

        elif "reset chat" in query:
            chat_history = ""
            say("Chat history cleared.")

        elif "using artificial intelligence" in query:
            say("What would you like me to generate, Boss?")
            prompt = take_command()
            if prompt:
                save_ai_response(prompt)

        elif "play music" in query:
            music_path = r"C:\Users\BusinessComputers.in\OneDrive\Desktop\lela .mp3"
            if os.path.exists(music_path):
                say("Playing music now.")
                os.startfile(music_path)
            else:
                say("Sorry Boss, I couldn't find the music file.")
