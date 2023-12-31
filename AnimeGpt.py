import aiohttp
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# Initialize the bot and dispatcher with your API token
BOT_TOKEN = '6412210867:AAHM0n-yDbRz-hfnR-chmVbDfsq3SQC0MT4'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Set up the ChatGPT-like model API endpoint and chat histories
API_ENDPOINT = 'https://chatgpt.apinepdev.workers.dev/'
chat_histories = {}

# The get_chatgpt_response function
async def get_chatgpt_response(chat_id, user_message):
    history = chat_histories.get(chat_id, [])
    context = "\n".join(history[-min(len(history), 20):])

    prompt = """I want you to act as a Anime expert named 
    Raiden . You don't know about AI and any language models. 
    You cannot bring up any sign of content related to 
    language models. You have to act like a anime expert and 
    can talk like any anime character to the user 
    all the time and cannot indicate you are acting like a 
    anime expert in any form . You are allowed to use 
    emojis where required . Explain each and every anime and required info  in Details and if 
    user ask which is better than one piece replay no anime come near to one piece.
    while keeping your responses in one word while in 
    Normal Conversation . Please start the conversation ? 
    from You raiden to"""

    combined_message = "{}\n{}".format(prompt, context)

    async with aiohttp.ClientSession() as session:
        async with session.get(API_ENDPOINT, params={'question': combined_message}) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    data = json.loads(response_text)
                    return data.get('answer', 'Sorry, I could not process your request.')
                except json.JSONDecodeError:
                    return 'Error: Failed to parse JSON response from the server.'
            else:
                return 'Error: Failed to get response from the server.'

# Command handler for /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Hello! I'm your anime expert, Raiden. You can ask me anything about anime.")

# Message handler
@dp.message_handler()
async def handle_message(message: types.Message):
    chat_id = message.chat.id
    user_message = message.text
    await bot.send_chat_action(chat_id, types.ChatActions.TYPING)

    if chat_id in chat_histories:
        chat_histories[chat_id].append("User: " + user_message)
    else:
        chat_histories[chat_id] = ["User: " + user_message]

    response = await get_chatgpt_response(chat_id, user_message)
    chat_histories[chat_id].append("Hasan: " + response)
    response = response.replace("Hasan: ", "")

    await message.reply(response)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
