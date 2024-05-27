import os
import json
from typing import Final
from dotenv import load_dotenv

from services.language.tools.tools import get_all_available_tools, get_tool_map
from services.common.utils.templater import load_template_file

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain.memory import ConversationBufferMemory
from langchain.agents import ConversationalChatAgent
from langchain.agents import AgentExecutor


load_dotenv("config.env")
GOOGLE_API_KEY: Final = os.environ.get("GOOGLE_API_KEY")
GOOGLE_PROJECT_ID: Final = os.environ.get("GOOGLE_PROJECT_ID")

def get_system_instructions() -> str:
    """
    Returns the system instructions that define how Alvin behaves when interacting with the user.
    """
    prompts = load_template_file('templates/prompts.yaml')
    return prompts["prompts"]["system"] + prompts["prompts"]["context"]

def get_standard_hello_message() -> str:
    commands = load_template_file('templates/commands.yaml')
    return f"Se apresente apenas uma vez e com base na mensagem: {commands['commands']['start']}. Seja breve, claro e não se esqueça de falar sobre a funcionalidade do SOS"

def say_hello(conversation: AgentExecutor) -> str:
    conversation.invoke(f"{get_standard_hello_message()}")
    return parse_content_response(extract_latest_response_from_memory(conversation.memory))

def extract_latest_response_from_memory(memory: ConversationBufferMemory) -> AIMessage:
    messages = memory.chat_memory.messages
    if messages != []:
        return messages[-1]
    return None

def get_chat_system_prompt_template(with_hello_message: bool = False) -> ChatPromptTemplate:
    if with_hello_message:
        return ChatPromptTemplate.from_messages(
            [
                ("system", get_system_instructions()),
                ("human", "{hello_message}")
            ]
        )
    return ChatPromptTemplate.from_messages([("system", get_system_instructions()), ("human", "")])

def parse_raw_chat_output(response: AIMessage) -> Runnable:
    tool_calls = response.tool_calls.copy()
    for tool_call in tool_calls:
        tool_call["output"] = get_tool_map()[tool_call["name"]].invoke(tool_call["args"])
    return response

def parse_chat_tool_response(user_message: str, response: AIMessage, chat_session: ChatGoogleGenerativeAI) -> str:
    """
        Parses the model response and return the full string message.
    """
    analyze_tool_response = ChatPromptTemplate.from_template(
        "Responda a messagem do usuário: {message}, com base no output: {tool_call}. Não mencione nada sobre a função em si"
    )

    chain = {"tool_call": RunnablePassthrough(), "message": RunnablePassthrough()} | analyze_tool_response | chat_session
    analyzed_response = chain.invoke(
        {"tool_call": f"{json.dumps(response.tool_calls)}", "message": f"{user_message}"}
    )
    
    return parse_content_response(analyzed_response)

def parse_content_response(response: AIMessage) -> str:
    """
        Parses the model response and return the full string message.
    """
    return response.content or "Ah não! Desculpa não consegui obter nenhuma informação :("


def start_chat_session(model: str, enable_tools: bool = True) -> ChatGoogleGenerativeAI:
    """
        Returns the chat started from the model.
    """
    llm = ChatGoogleGenerativeAI(model=model, google_api_key=GOOGLE_API_KEY)
    if enable_tools:
        llm = llm.bind_tools(get_all_available_tools())
    return llm

def start_conversation(chat_session: ChatGoogleGenerativeAI, enable_tools: bool = True) -> AgentExecutor:
    tools = get_all_available_tools() if enable_tools else []
    
    agent = ConversationalChatAgent.from_llm_and_tools(
        llm=chat_session,
        tools=tools,
        system_message=get_system_instructions()
    )

    executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=ConversationBufferMemory(
            human_prefix="user",
            ai_prefix="assistant",
            memory_key="chat_history",
            return_messages=True
        )
    )
    executor.verbose = True

    return executor


def get_response_to_user_message(user_message: str, conversation: AgentExecutor) -> str:
    """
        Returns response to user messsage
    """
    conversation.invoke(user_message)
    return parse_content_response(extract_latest_response_from_memory(conversation.memory))


if __name__ == "__main__":
    chat = start_chat_session(model="gemini-1.5-flash")
    conversation = start_conversation(chat)
    print(say_hello(conversation))

    while True:
        prompt = input("Pergunte alguma coisa: ")
        if (prompt == "exit"):
            break
        response = get_response_to_user_message(prompt, conversation)
        print(response)

