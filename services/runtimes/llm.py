from ollama import Client
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]  # adjust as needed
CONFIG_PATH = ROOT_DIR / "config.json"
API_PATH = ROOT_DIR / "ollama_key.txt"
#get config
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)
    
with open(API_PATH, "r") as f:
  api_key = f.readline()

LANGUAGE_MODEL = config["LANGUAGE_MODEL"]

# temporarily empty
retrieved_knowledge = ""

# create an instruction prompt for the chatbot - temp
instruction_prompt = config["INSTRUCTION_PROMPT"]



def get_response(query, context):
    if context is None:
      context_str = ""
    elif not isinstance(context, str):
      context_str = str(context)
    else:
      context_str = context
    response = ""
    
    #open stream to model locally and send message
#    stream = ollama.chat(
#    model=LANGUAGE_MODEL,
#    messages=[
#      {'role': 'system', 'content': instruction_prompt},
#      {'role': 'system', 'content': context},
#      {'role': 'user', 'content': query},
#    ],
#    stream=True,
#    )
    
    #open ollama on turbo with api key
    client = Client(
      host = "https://ollama.com",
      headers={'Authorization': api_key}
    )
    
    messages=[
      {'role': 'system', 'content': instruction_prompt},
      {'role': 'system', 'content': context},
      {'role': 'user', 'content': query},
    ]
  
  

  #return output from local
#   for chunk in stream:
 #     if "message" in chunk and "content" in chunk["message"]:
  #        content = chunk["message"]["content"]
  #        print(content, end="", flush=True)   # live CLI output
  #        response += content             # accumulate

  #return response from turbo
    for part in client.chat('gpt-oss:120b', messages=messages, stream=True):
      content = part["message"]["content"]
      print(content, end='', flush=True)
      response+= content
      
    return response