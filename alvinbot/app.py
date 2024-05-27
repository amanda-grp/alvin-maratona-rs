from typing import Final
from functools import partial
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
from langchain.agents import AgentExecutor

# Command management
from services.bot.commands import start, error, nearby_shelters, location_input
from services.common.utils.templater import load_template_file
from services.location.location import get_haversine_distance
from services.language.llm import start_chat_session, start_conversation, get_response_to_user_message, extract_latest_response_from_memory, say_hello

load_dotenv("config.env")
TELEGRAM_BOT_TOKEN: Final = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_USERNAME: Final = os.environ.get("TELEGRAM_BOT_USERNAME")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

commands = load_template_file("templates/commands.yaml")
prompts = load_template_file("templates/prompts.yaml")

#### Response and Message Handling ####
def handle_free_text_response(text: str, chat_session: AgentExecutor) -> str:
    # normalizes user's input for LLM processing
    user_message: str = text.lower()
    return get_response_to_user_message(user_message, chat_session)

async def handle_free_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE, conversation: AgentExecutor
):
    if (extract_latest_response_from_memory(conversation.memory) is None) and ('bot_already_started' in context.user_data):
        agent_response = say_hello(conversation)
        print("Bot: ", agent_response)

    else:
        user_message: str = update.message.text
        agent_response: str = handle_free_text_response(user_message, conversation)
        print("User: ", user_message)
        print("Bot: ", agent_response)

    await update.message.reply_text(agent_response)


if __name__ == "__main__":
    print("Starting Alvin ...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handling
    app.add_handler(
        CommandHandler("quemsoueu", partial(start, command_strings=commands))
    )

    app.add_handler(
        CommandHandler("start", partial(start, command_strings=commands))
    )

    app.add_handler(
        CommandHandler(
            "abrigosproximos", partial(nearby_shelters, command_strings=commands)
        )
    )

    # Message handling
    chat = start_chat_session(model="gemini-1.5-flash")
    conversation = start_conversation(chat)

    app.add_handler(
        MessageHandler(
            filters.TEXT, partial(handle_free_text_message, conversation=conversation)
        )
    )
    
    app.add_handler(MessageHandler(filters.LOCATION, location_input))

    # Error handling
    app.add_error_handler(partial(error, command_strings = commands))

    # Polling the bot
    print("Polling ...")
    app.run_polling(poll_interval=3)
