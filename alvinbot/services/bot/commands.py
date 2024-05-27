from typing import Final, NewType, Tuple
import pandas as pd
import json

# Telegram integration
from telegram import Update
from telegram.ext import (
    filters,
    ContextTypes,
)
from services.location.location import get_haversine_distance

Coordinate = NewType(name="Coordinates", tp=Tuple[float, float])


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE, command_strings: dict
):
    """Comando de começo padrão do Alvin
    Retorna uma breve instrução sobre o que ele pode fazer e descreve as abilidades existentes
    """
    start_response = command_strings["commands"]["start"]

    await update.message.reply_text(start_response)


async def location_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recebe uma mensagem contendo localização do usuário e retorna respostas relacionadas a essa localização"""
    message_latitude = update.message.location.latitude
    message_longitude = update.message.location.longitude
    current_location = Coordinate((message_latitude, message_longitude))
    context.user_data["current_location"] = current_location
    await update.message.reply_text(
        f"Obrigado por enviar sua localização, por favor tente usar o comando /abrigosproximos novamente!"
    )


async def nearby_shelters(
    update: Update, context: ContextTypes.DEFAULT_TYPE, command_strings: dict
):
    """Comando de começo padrão do Alvin
    Retorna uma breve instrução sobre o que ele pode fazer e descreve as abilidades existentes
    """
    no_location_shared_response = command_strings["commands"]["nearby_shelters"][
        "error_states"
    ]["no_location_shared"]

    if "current_location" not in context.user_data:
        await update.message.reply_text(no_location_shared_response)

    else:
        # Processes the nearby shelters
        # simulates a database query / api call
        with open("./data/tables/entidades.json", "r") as input_file:
            entities = pd.DataFrame(json.load(input_file))

        entities = entities.assign(
            distance=entities.apply(
                lambda row: get_haversine_distance(
                    context.user_data["current_location"],
                    Coordinate((row.latitude, row.longitude)),
                ),
                axis=1,
            )
        )

        # limits to the closest 3 shelters
        nearest_shelters = (
            entities.nsmallest(3, "distance")[["nome", "endereco", "site", "telefone"]].fillna('N/A')
            .set_index("nome")
            .to_dict(orient="index")
        )

        response = "Os abrigos mais próximos de você são:\n"

        for shelter, info in nearest_shelters.items():
            info_string = f"\n{shelter}\n\n{info['endereco']}\n({info['telefone']})\n\n"
            response += info_string

        await update.message.reply_text(f"{response}")


async def error(
    update: Update, context: ContextTypes.DEFAULT_TYPE, command_strings: dict
):
    """Gestão de erros, utilizada quando um erro é encontrado no bot para definir resposta padrão ao usuário"""
    print(f"Update {update} caused error {context.error}")
    error_response = command_strings["commands"]["error"]
    await update.message.reply_text(error_response)
