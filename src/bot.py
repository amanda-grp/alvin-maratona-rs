from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

load_dotenv("config.env")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
telegram_bot_username = os.environ.get("TELEGRAM_BOT_USERNAME")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """ 
Olá! Eu sou o Alvin, seu assistente de benfeitorias. O Brasil todo está se esforcando para ajudar nossos companheiros do Rio Grande do Sul. Aqui você pode procurar por oportunidades e vias de doacao. 
"""
    )


# handling responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "alvin" in processed:
        return "Meu nome é Alvin, e eu sou um assistente de benfeitorias"

    return "Não entendi o que você perguntou, poderia tentar novamente?"


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
    app = Application.builder().token(telegram_bot_token).build()

    # handles the commands
    app.add_handler(CommandHandler("comecar", start_command))

    # handles the messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # same for errors
    app.add_error_handler(error)

    # Polling the bot
    print("Polling...")
    app.run_polling(poll_interval=3)
