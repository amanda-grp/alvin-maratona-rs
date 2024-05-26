from typing import Final
from templater import load_commands

# Telegram integration
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, command_strings: dict):
    """Comando de começo padrão do Alvin
    Retorna uma breve instrução sobre o que ele pode fazer e descreve as abilidades existentes
    """
    start_response = command_strings["commands"]["start"]

    await update.message.reply_text(
        start_response
    )