import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai
import sys 

class Reference:
    def __init__(self) -> None:
        '''
        This class to store previousely response from the chatGpt API
        '''
        self.response = ""

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

reference = Reference()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

#Model name
MODEL_NAME = "gpt-3.5-turbo"

#Intialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher (bot)

def clear_past():
    """
    A function to clear the previous conversation and context.
    """
    reference.response = ""


@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives message with `/start` or `/help` command 
    """
    await message.reply("Hi\nI am Tele Bot!\nCreated by pwskills. How can i assit you?")



@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """ 
    clear_past()
    await message.reply("I have cleared the past message and context.")



@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to deisplay the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by PWskills! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using chatGpt API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = MODEL_NAME,
        message = [
            {"role": "assistance", "content": reference.response}, #role assistant
            {"role": "user", "content": message.text} #our query
        ]
    )
    reference.response = response.choices[0]['message']['content']
    print(f">>> chatGpt: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response)

if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates = True)