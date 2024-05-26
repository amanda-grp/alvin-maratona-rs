
import maritalk
from dotenv import load_dotenv
import os

load_dotenv("config.env")
MARITALK_API_KEY = os.environ.get("MARITALK_API_KEY")
model = maritalk.MariTalk(key=MARITALK_API_KEY, model="sabia-2-medium")
answer = model.generate("Quanto é 25 + 27?")
print(f"Resposta: {answer}")  

