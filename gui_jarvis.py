import os
import pyautogui
import psutil
import subprocess
import webbrowser
import speech_recognition as sr
import pyttsx3
engine=pyttsx3.init()
engine.setProperty("rate",150)
voices=engine.getProperty("voices")
engine.setProperty("voice",voices[0].id)
import google.generativeai as genai
from dotenv import load_dotenv
from tkinter import scrolledtext
import tkinter as tk
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model=genai.GenerativeModel("gemini-flash-latest",system_instruction="You are jarvis ")
chat=model.start_chat(history=[])
def speak(text):
    engine.say(text)
    engine.runAndWait()
def start_listening():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        chat_history.insert(tk.END,"Listening...\n")
        root.update()
        try:
            audio=r.listen(source,timeout=5)
            text=r.recognize_google(audio)
            user_input.delete(0,tk.END)
            user_input.insert(0,text)
            send_message()
        except:
            chat_history.insert(tk.END,"i dint catch that\n")
def send_message(event=None):
    prompt=user_input.get()
    if prompt:
        chat_history.insert(tk.END,"YOU:" +prompt+"\n")
        prompt_lower=prompt.lower()
        if "open youtube " in prompt_lower:
            speak("Opening Youtube for u jamshee")
            webbrowser.open("https://www.youtube.com")
            user_input.delete(0,tk.END)
            return
        elif "open google" in prompt_lower:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
            user_input.delete(0,tk.END)
            return
        # --- SYSTEM ADMIN COMMANDS ---
        
        elif "open notepad" in prompt_lower:
            speak("Opening Notepad.")
            os.system("start notepad") # Windows command
            user_input.delete(0, tk.END)
            return

        elif "open calculator" in prompt_lower:
            speak("Opening Calculator.")
            os.system("start calc")
            user_input.delete(0, tk.END)
            return

        elif "shutdown system" in prompt_lower:
            speak("Shutting down the system in 5 seconds. Goodbye sir.")
            # /s = shutdown, /t 5 = wait 5 seconds
            os.system("shutdown /s /t 5") 
            user_input.delete(0, tk.END)
            return
            
        elif "restart system" in prompt_lower:
            speak("Restarting system.")
            os.system("shutdown /r /t 5")
            user_input.delete(0, tk.END)
            return
        # --- HARDWARE CONTROL ---
        
        elif "volume up" in prompt_lower:
            pyautogui.press("volumeup")
            speak("Volume increased.")
            user_input.delete(0, tk.END)
            return
            
        elif "volume down" in prompt_lower:
            pyautogui.press("volumedown")
            speak("Volume decreased.")
            user_input.delete(0, tk.END)
            return
            
        elif "mute" in prompt_lower:
            pyautogui.press("volumemute")
            speak("System muted.")
            user_input.delete(0, tk.END)
            return
            
        elif "screenshot" in prompt_lower:
            speak("Taking screenshot.")
            # Saves it as 'screenshot.png' in the same folder
            pyautogui.screenshot("screenshot.png") 
            speak("Screenshot saved.")
            user_input.delete(0, tk.END)
            return

        # --- SYSTEM HEALTH ---

        elif "battery" in prompt_lower or "power" in prompt_lower:
            battery = psutil.sensors_battery()
            percent = battery.percent
            plugged = battery.power_plugged
            
            status = "plugged in" if plugged else "running on battery"
            speak(f"System is at {percent} percent and is {status}.")
            
            chat_history.insert(tk.END, f"Jarvis: Battery is {percent}% ({status})\n\n")
            user_input.delete(0, tk.END)
            return
            
        # -----------------------------
        response=chat.send_message(prompt)
        chat_history.insert(tk.END,"Jarvis: "+ response.text +"\n\n")
        speak(response.text)
        user_input.delete(0,tk.END)
        

root=tk.Tk()
root.title("JARVIS AI")
root.geometry("500x600")
root.configure(bg="white")
chat_history=scrolledtext.ScrolledText(root,width=50,height=20,bg="black",fg="cyan",font=("Arial",12))
chat_history.pack(pady=10)
user_input=tk.Entry(root,width=40,bg="black",fg="white",insertbackground="white")
user_input.pack(pady=5)
send_btn=tk.Button(root,text="Send",command=send_message,bg="cyan",fg="black")
send_btn.pack(pady=5)
mic_btn=tk.Button(
    root,
    text="speak",
    command=start_listening,
    bg="#202020",
    fg="white",
    font=("Arial",10,"bold")
)
mic_btn.pack(pady=5)
root.bind('<Return>',send_message)
root.mainloop()
