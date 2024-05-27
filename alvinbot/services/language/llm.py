import os
from dotenv import load_dotenv
import google.generativeai as genai

from services.language.tools.tools import get_all_available_tools
from services.common.templater import load_template_file

load_dotenv("config.env")
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def get_system_instructions() -> str:
    """
        Returns the system instructions that define how Alvin behaves when interacting with the user.
    """
    prompts = load_template_file(
        'templates/prompts.yaml'
    )

    return prompts["prompts"]["system"] + prompts["prompts"]["context"],

def start_model(enable_tools:bool = True) -> genai.GenerativeModel:
    """
        Returns the generative model based on the system instructions and available tools.
    """
    tools = get_all_available_tools() if enable_tools else []

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=get_system_instructions(),
        tools=tools
    )

def start_chat_session(model: genai.GenerativeModel) -> genai.ChatSession:
   """
    Returns the chat started from the model.
   """
   return model.start_chat(history=[], enable_automatic_function_calling=True)

def get_response_to_user_message(user_message: str, chat_session: genai.ChatSession) -> str:
    """
        Returns response to user messsage
    """
    response = chat_session.send_message(user_message, stream=False)
    return parse_response(response)

def parse_response(response: list) -> str:
  """
    Parses the model response and return the full string message.
  """
  full_response = ""
  for chunk in response:
    full_response += chunk.text

  return full_response

if __name__ == "__main__":
    model = start_model()
    chat = start_chat_session(model)

    while True:
        prompt = input("Pergunte alguma coisa: ")
        if (prompt == "exit"):
            break
        response = get_response_to_user_message(prompt, chat)
        print(response)