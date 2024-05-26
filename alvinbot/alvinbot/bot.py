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
from templater import load_commands

load_dotenv("config.env")
TELEGRAM_BOT_TOKEN: Final = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_USERNAME: Final = os.environ.get("TELEGRAM_BOT_USERNAME")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Sets up the credentials for gemini calls
genai.configure(api_key=GOOGLE_API_KEY)

# Loads commands:
commands = load_commands(
    'templates/commands.yaml'
)

# handling responses
def handle_response(text: str) -> str:

    processed: str = text.lower()

    # output_parser = StrOutputParser()

    # chat_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             system_prompt["system"],
    #         ),
    #         ("human", "Eu tenho {item} para doar"),
    #     ]
    # )

    # chain = chat_prompt | llm | output_parser

    # response = chain.invoke({"item": processed})

    return 'Estou em desenvolvimento ainda, volte depois!'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(
        f'Usuario: {update.message.chat.id} mandou uma mensagem no {message_type}: "{text}"'
    )
    response: str = handle_response(text)

    print("Bot: ", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting Alvin ...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # handles the commands
    app.add_handler(CommandHandler("comecar", partial(start, command_strings = commands)))

    # handles the messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # same for errors
    app.add_error_handler(error)

    # Polling the bot
    print("Polling ...")
    app.run_polling(poll_interval=3)
