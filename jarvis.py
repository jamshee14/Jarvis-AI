import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model=genai.GenerativeModel("gemini-flash-latest")
chat=model.start_chat(history=[])
def run_chat():
    print("welcome your bot is online")
    while True:
        user_input=input(" ")
        if user_input=="quit":
            print("goodbye")
            break
        response=chat.send_message(user_input)
        print(response.text)

if __name__=="__main__":
    run_chat()
