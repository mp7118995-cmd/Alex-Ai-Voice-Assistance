import speech_recognition as sr
import datetime
import webbrowser
import os
import requests
import re
import edge_tts
import asyncio
import pygame
import time
import pyautogui
import pyperclip
import subprocess


pygame.mixer.init()


contacts = {
    "myself": {"name": "+91 97666 30675", "phone": "+919766630675"},
    "mom":    {"name": "Mom Name",        "phone": "+91XXXXXXXXXX"},
    "dad":    {"name": "Dad Name",        "phone": "+91XXXXXXXXXX"},
    "friend": {"name": "Friend Name",     "phone": "+91XXXXXXXXXX"},
}

def ollama_run():
    try:
        r = requests.get("http://localhost:11434", timeout=3)
        return True
    except:
        return False

def alex(prompt):
    try:
        if not ollama_run():
            speak("Ollama is not running. Please start it.")
            return ""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",  # changed from llama3 to llama3.2
                "prompt": f"Answer in 1-2 sentences only, no extra text: {prompt}",
                "stream": False
            },
            timeout=60
        )
        return response.json()["response"]
    except requests.exceptions.Timeout:
        print("Ollama timeout - model is slow")
        return "Sorry, AI is taking too long. Please try again."
    except Exception as e:
        print("AI Error:", e)
        return "AI is not running. Please start Ollama."


def clean_text(text):
    text = re.sub(r'[*#`_>\-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_com(command):
    return command.replace("alex", "").strip()


def speak(text):
    try:
        print("Speaking:", text)
        text = clean_text(text)

        # Generate and play in one shot
        async def generate_and_play():
            communicate = edge_tts.Communicate(text, voice="en-US-ChristopherNeural")
            await communicate.save("reply.mp3")

        asyncio.run(generate_and_play())

        pygame.mixer.music.load("reply.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05) 
        pygame.mixer.music.unload()
        os.remove("reply.mp3")

    except Exception as e:
        print("Speak error:", e)


def send_whatsapp(command):
    try:
        command = command.replace("alex", "").strip()
        command = command.replace("send whatsapp", "").strip()
        command = command.replace("whatsapp", "").strip()
        command = command.replace("send message", "").strip()
        command = command.replace("to", "", 1).strip()

        print("Cleaned WhatsApp command:", command)
        words = command.split(" ", 1)

        if len(words) < 2:
            speak("Please say the contact name and then the message.")
            return

        contact_name = words[0].strip()
        message = words[1].strip()

        if contact_name not in contacts:
            speak(f"Contact {contact_name} not found.")
            return

        full_name = contacts[contact_name]["name"]
        speak(f"Sending message to {contact_name}.")

        os.system("start whatsapp:")
        time.sleep(4)  

        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.5)     

        pyperclip.copy(full_name)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1.5)  

        pyautogui.press('enter')
        time.sleep(0.5)  

        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3) 
        pyautogui.press('enter')

        speak("Message sent.")

    except Exception as e:
        print("WhatsApp error:", e)
        speak("Failed to send message.")


close_apps = {
    "chrome":    "chrome.exe",
    "google":    "chrome.exe",
    "youtube":   "chrome.exe",
    "whatsapp":  "WhatsApp.exe",
    "setup":    "Cursor.exe",
    "notepad":   "notepad.exe",
    "spotify":   "Spotify.exe",
    "vlc":       "vlc.exe",
    "word":      "WINWORD.EXE",
    "excel":     "EXCEL.EXE",
}

def close_app(command):
    try:
        # Clean command
        command = command.replace("alex", "").strip()
        command = command.replace("close", "").strip()
        command = command.replace("shut", "").strip()
        command = command.replace("exit", "").strip()
        command = command.strip()

        print("App to close:", command)

        matched = None
        for key in close_apps:
            if key in command:
                matched = close_apps[key]
                break

        if matched is None:
            speak(f"I don't know how to close {command}.")
            return

        result = os.system(f"taskkill /f /im {matched}")

        if result == 0:
            speak(f"Closed {command} successfully.")
        else:
            speak(f"Could not close {command}. It may not be running.")

    except Exception as e:
        print("Close error:", e)
        speak("Failed to close the application.")



r = sr.Recognizer()
r.energy_threshold = 300       
r.dynamic_energy_threshold = True 

def take_command():
    with sr.Microphone() as source:
        print("Listening...")

        try:
            
            audio = r.listen(source, timeout=4, phrase_time_limit=6)
            command = r.recognize_google(audio)
            print("You said:", command)
            return command.lower()

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except sr.UnknownValueError:
            print("Could not understand.")
            return ""

        except sr.RequestError as e:
            print("Google API error:", e)
            return ""

        except Exception as e:
            print("Error:", e)
            return ""


def run_alex():
   
    print("Calibrating mic...")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
    print("Mic ready.")

    speak("Alex Activated Boss. Whats new today?")

    while True:
        command = take_command()

        if command == "":
            continue

       
        if "time" in command:
            t = datetime.datetime.now().strftime("%H:%M")
            speak("Current time is " + t)

        
        elif "whatsapp" in command or "send message" in command:
            send_whatsapp(command)

        
        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")

        elif "open google" in command:
            webbrowser.open("https://google.com")
            speak("Opening Google")

        elif "open chrome" in command:
            os.system("start chrome")
            speak("Opening Chrome")

        elif "open cursor" in command or "open setup" in command:
            try:
                speak("Opening Cursor")
                subprocess.Popen(["powershell", "-Command", "cursor"])
            except Exception as e:
                print("Cursor error:", e)
                speak("Failed to open Cursor.")

        
        elif "close" in command or "shut down" in command:
            close_app(command)

        
        elif "stop" in command:
            speak("Goodbye! See you again soon.")
            break

        
        else:
            cleaned = clean_com(command)
            print("Sending to AI:", cleaned)
            reply = alex(cleaned)
           # print("AI replied:", reply)
            if reply and reply.strip() != "":
                speak(reply)
            else:
                speak("No response from AI.")

run_alex()
