from typing import Final
from functools import partial
import textwrap
import requests
import json
import os

# Telegram integration
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

# LLM integration
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate

# Command management
from default_commands import start
from templater import load_template_file

load_dotenv("config.env")
TELEGRAM_BOT_TOKEN: Final = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_USERNAME: Final = os.environ.get("TELEGRAM_BOT_USERNAME")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Sets up the credentials for gemini calls
genai.configure(api_key=GOOGLE_API_KEY)

# Loads commands:
commands = load_template_file(
    'templates/commands.yaml'
)

prompts = load_template_file(
    'templates/prompts.yaml'
)

# handling responses
def handle_response(text: str, prompt_template: dict) -> str:

    user_message: str = text.lower()
    output_parser = StrOutputParser()

    llm = ChatGoogleGenerativeAI(
        model = 'gemini-1.5-flash'
    )

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt_template["prompts"]["system"] + prompt_template["prompts"]["context"],
            ),
            (
                "human",    
                f"{user_message}"
            ),
        ]
    )

    chain = chat_prompt | llm | output_parser

    response = chain.invoke({"user_message": user_message})

    return response


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt_template: dict):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(
        f'User data from message: {update.message.from_user}\nMessage: {text}'
    )

    response: str = handle_response(text, prompt_template)

    print("Bot: ", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.location)

if __name__ == "__main__":
    print("Starting Alvin ...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # handles the commands
    app.add_handler(CommandHandler("comecar", partial(start, command_strings = commands)))

    # handles the messages
    app.add_handler(MessageHandler(filters.TEXT, partial(handle_message, prompt_template=prompts)))
    app.add_handler(MessageHandler(filters.LOCATION, location))

    # same for errors
    app.add_error_handler(error)

    # Polling the bot
    print("Polling ...")
    app.run_polling(poll_interval=3)
