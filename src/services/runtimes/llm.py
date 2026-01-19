import ollama
from ollama import Client
from core.config import load_config, load_api_key

config = load_config()
api_key = load_api_key()

LANGUAGE_MODEL = config["LANGUAGE_MODEL"]

# temporarily empty
retrieved_knowledge = ""

# create an instruction prompt for the chatbot - temp
instruction_prompt = config["INSTRUCTION_PROMPT"]

#variable for local inference
local = config["LOCAL_INFERENCE"]

def get_response(query, context):
    if context is None:
      context_str = ""
    elif not isinstance(context, str):
      context_str = str(context)
    else:
      context_str = context
    response = ""
    
    if local == True:
      #open stream to model locally and send message
      stream = ollama.chat(
      model=LANGUAGE_MODEL,
      messages=[
        {'role': 'system', 'content': instruction_prompt},
        {'role': 'system', 'content': context_str},
        {'role': 'user', 'content': query},
      ],
      stream=True,
      )
      
        #return output from local
      for chunk in stream:
        if "message" in chunk and "content" in chunk["message"]:
          content = chunk["message"]["content"]
          print(content, end="", flush=True)   # live CLI output
          response += content             # accumulate

    elif api_key != "":
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
    
    #return response from turbo
      for part in client.chat(LANGUAGE_MODEL, messages=messages, stream=True):
        content = part["message"]["content"]
        print(content, end='', flush=True)
        response+= content
    
    else:
      response = "Error: No API key set for Ollama-hosted models. Please set your API key or enable local inference. ragforge set-ollama-api-key <your_api_key>"
      
    return response