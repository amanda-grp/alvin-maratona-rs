from typing import Final, NewType, Tuple

# Telegram integration
from telegram import Update
from telegram.ext import (
    filters,
    ContextTypes,
)

Coordinate = NewType(
    name = "Coordinates",
    tp = Tuple[float, float]
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, command_strings: dict):
    """Comando de começo padrão do Alvin
    Retorna uma breve instrução sobre o que ele pode fazer e descreve as abilidades existentes
    """
    start_response = command_strings["commands"]["start"]

    await update.message.reply_text(
        start_response
    )

async def location_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe uma mensagem contendo localização do usuário e retorna respostas relacionadas a essa localização
    """
    current_user_location = update.message.location

    await update.message.reply_text(
        f'Você está em {current_user_location}'
    )

async def nearby_shelters(update: Update, context: ContextTypes.DEFAULT_TYPE, command_strings: dict):
    """Comando de começo padrão do Alvin
    Retorna uma breve instrução sobre o que ele pode fazer e descreve as abilidades existentes
    """
    no_location_shared_response = command_strings["commands"]["nearby_shelters"]["error_states"]["no_location_shared"]

    if 'current_location' not in context.user_data:
        await update.message.reply_text(
            no_location_shared_response
        )

    else:
        # processes the nearby shelters
        result = Coordinates(update.message.location)
        print(result, type(result))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE, command_strings: dict):
    """Gestão de erros, utilizada quando um erro é encontrado no bot para definir resposta padrão ao usuário
    """
    print(f"Update {update} caused error {context.error}")
    error_response = command_strings["commands"]["error"]
    await update.message.reply_text(error_response)
