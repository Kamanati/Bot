import telebot
from telebot import types
from time import *
# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather on Telegram
bot = telebot.TeleBot('6351546641:AAELLoxwNgVCLNrqmTWortcu_0lwUrM0Mkk')

# Dictionary to store user chat codes
user_chats = {}
message_ids = {}  # Store message IDs sent by the bot
chat_history = {}
your_message = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to your private chat bot! Use\n usage /chat [code] to start a private chat.\nuse /help to see instruction of this bot")

@bot.message_handler(commands=['help'])
def handle_help(message):
    chat_id = message.chat.id
    webapp_url = "http://t.me/Private_chat_ai_bot/Help"
    
    # Send the web app URL as a message with an inline keyboard button
    markup = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="View detailed instruction", url=webapp_url)
    markup.add(url_button)
    
    bot.send_message(chat_id, "Click the button below to open detailed instruction:", reply_markup=markup)

@bot.message_handler(commands=['chat'])
def handle_chat(message):
    chat_code = message.text[6:]  # Extract chat code
    user_chats[message.chat.id] = chat_code

    creator_chat_id = get_chat_creator(chat_code)
    if chat_code != "":
 #    bot.send_message(message.chat.id, "please enter the chat code. use /help to see instruction")
        pass
    else:
        bot.send_message(message.chat.id, "please enter the chat code. use /help to see instruction")
        
    if creator_chat_id:
        if creator_chat_id == message.chat.id:
            bot.send_message(message.chat.id, f"You created the chat code. tell the user to join tha chat with this code /chat {chat_code}")
        else:
            creator_user = bot.get_chat_member(creator_chat_id, creator_chat_id).user
            creator_name = f"{creator_user.first_name} {creator_user.last_name}"
            bot.send_message(message.chat.id, f"Now you can chat with {creator_name}.")
    else:
        bot.send_message(message.chat.id, f"This chat code does not have a creator.")
 #   else:
  #   bot.send_message(message.chat.id, "please enter the chat code. use /help to see instruction")
#     pass
# Function to get the creator's chat ID based on the chat code
def get_chat_creator(chat_code):
    for chat_id, code in user_chats.items():
        if code == chat_code:
            return chat_id
    return None
"""
@bot.message_handler(commands=['chat'])
def handle_chat(message):
    user_chats[message.chat.id] = message.text[6:]  # Extract chat code
    bot.send_message(message.chat.id, f"You can now chat privately with code: {user_chats[message.chat.id]}")
"""
@bot.message_handler(commands=['safe'])
def handle_safe_command(message):
    clear_chat(message)

@bot.message_handler(func=lambda message: message.chat.id in user_chats)
def handle_private_chat(message):
    chat_code = user_chats[message.chat.id]
    for user_id, code in user_chats.items():
        if user_id != message.chat.id and code == chat_code:
            # Store the message ID for messages sent by the bot
            message_id = bot.send_message(user_id, f"Private message from {message.from_user.first_name}: {message.text}").message_id
            bot.delete_message(message.chat.id, message.message_id)
#            your_message.append(message.message_id)

            if user_id in message_ids:
                message_ids[user_id].append(message_id)
            else:
                message_ids[user_id] = [message_id]
            if user_id in chat_history:
                pass
            else:
                chat_history[user_id] = [f"{message.from_user.first_name}: {message.text}"]

def clear_chat(message):
    chat_id = message.chat.id
    if chat_id in user_chats:
 #       del user_chats[chat_id]  # Remove the chat from the dictionary
 #       for your_message in yrm:
  #             bot.delete_message(chat_id, yrm)
        # Delete bot's messages in the chat
        if chat_id in message_ids:
            for message_id in message_ids[chat_id]:
                bot.delete_message(chat_id, message_id)
            bot.send_message(chat_id, 'Chat history cleared')
            del message_ids[chat_id]
        else:
            bot.send_message(chat_id, 'No messages to clear in your chat history')
    else:
        bot.send_message(chat_id, 'You are not currently in a private chat')
        sleep(19)

bot.polling()
