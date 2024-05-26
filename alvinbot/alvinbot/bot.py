from typing import Final
import json
import os

# Telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# LLM integration
from langchain_community.chat_models import ChatMaritalk
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate

load_dotenv("config.env")
TELEGRAM_BOT_TOKEN: Final = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_USERNAME: Final = os.environ.get("TELEGRAM_BOT_USERNAME")
MARITALK_API_KEY = os.environ.get("MARITALK_API_KEY")

llm = ChatMaritalk(
    model="sabia-2-small",
    api_key=MARITALK_API_KEY,  
    temperature=0.7,
    max_tokens=100
)

# read the system message:
with open('system_prompts.json', 'r') as input_file:
    system_prompt = json.load(input_file)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """ 
Olá! Eu sou o Alvin, seu assistente de benfeitorias. O Brasil todo está se esforcando para ajudar nossos companheiros do Rio Grande do Sul. Aqui você pode procurar por oportunidades e vias de doacao. 
"""
)

# handling responses
def handle_response(text: str) -> str:

    processed: str = text.lower()

    output_parser = StrOutputParser()

    chat_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt["system"],
            ),
            (
                "human", 
                "Eu tenho {item} para doar"
            ),
        ]
    )

    chain = chat_prompt | llm | output_parser

    response = chain.invoke({"item": processed})

    return response


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'Usuario: {update.message.chat.id} mandou uma mensagem no {message_type}: "{text}"')
    response: str = handle_response(text)

    print("Bot: ", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting Bot...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # handles the commands
    app.add_handler(CommandHandler("comecar", start_command))

    # handles the messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # same for errors
    app.add_error_handler(error)

    # Polling the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
