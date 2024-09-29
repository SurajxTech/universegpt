import telebot  
import requests  
from flask import Flask  
import time  

app = Flask(__name__)  

@app.route('/')  
def home():  
    return "Hello, I'm alive!"  

# Prompt for the Telegram bot token when the program runs  
bot_token = input("Enter your Telegram bot token: ")  

# Initialize the Telegram bot  
bot = telebot.TeleBot(bot_token)  

# API key for the AI service  
api_key = "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"  

# Set up headers for the AI service  
headers = {  
    "Authorization": 'Bearer ' + api_key,  
}  

# Function to get AI response with error handling  
def get_ai_response(question):  
    params = {  
        "messages": [  
            {  
                "role": 'user',  
                "content": question  
            }  
        ],  
        "model": 'gpt-4o'  
    }  

    try:  
        response = requests.post(  
            "https://aigptx.top/v1/chat/completions",  
            headers=headers,  
            json=params  
        )  
        response.raise_for_status()  # This will raise an error if the request was unsuccessful  
        res = response.json()  

        # Check if 'choices' exists in the response  
        if 'choices' in res and len(res['choices']) > 0:  
            return res['choices'][0]['message']['content']  
        else:  
            return "Error: Invalid response from the AI service. No 'choices' field found."  

    except requests.exceptions.RequestException as e:  
        # Handle connection errors, timeout, etc.  
        return f"Error: Failed to connect to the AI service. {str(e)}"  
    except Exception as e:  
        # Catch any other errors  
        return f"Error: {str(e)}"  

# Function to handle the /search command  
@bot.message_handler(commands=['search'])  
def search_command(message):  
    # Extract the search query after the /search command  
    search_query = message.text[len('/search '):]  

    if search_query.strip() == "":  
        bot.send_message(message.chat.id, "Please enter a search query after /search.")  
    else:  
        bot.send_message(message.chat.id, f"Searching for: {search_query}")  

        # Send the search query to the AI model  
        ai_response = get_ai_response(search_query)  

        # Send the AI's response back to the user  
        bot.send_message(message.chat.id, ai_response)  

# Function to handle regular messages  
@bot.message_handler(func=lambda message: True)  
def handle_message(message):  
    user_question = message.text  
    bot.send_message(message.chat.id, "Processing your question...")  

    # Send the user's question to the API  
    ai_response = get_ai_response(user_question)  

    # Send the AI's response back to the user  
    bot.send_message(message.chat.id, ai_response)  

# Start the bot  
if __name__ == '__main__':  
    from threading import Thread  
    Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5000}).start()  

    while True:  
        try:  
            bot.polling()  
        except Exception as e:  
            print(f"Bot polling error: {str(e)}")  
            time.sleep(15)
