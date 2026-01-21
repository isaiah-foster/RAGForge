import ollama
from ollama import Client
from core.config import load_server_config, load_ollama_api_key
from server.retrieval import retrieve

config = load_server_config()
api_key = load_ollama_api_key()

LANGUAGE_MODEL = config["LANGUAGE_MODEL"]

# temporarily empty
retrieved_knowledge = ""

#variable for local inference
local = config["LOCAL_INFERENCE"]

def stream_response(query, user_input):
    context = retrieve(user_input)
    if context is None:
      context_str = ""
      instruction_prompt = "You are a helpful AI assistant." #don't use rag prompt if no context
    elif not isinstance(context, str):
      context_str = str(context)
      instruction_prompt = config["INSTRUCTION_PROMPT"]
    else:
      context_str = context
      instruction_prompt = config["INSTRUCTION_PROMPT"]
    
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
            # ollama python lib typically returns: {"message":{"role":"assistant","content":"..."}}
            content = chunk.get("message", {}).get("content")
            if content:
                yield content

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
        content = part.get("message", {}).get("content")
        if content:
          yield content
    
    else:
      yield ("Error: No API key set for Ollama-hosted models."
                  "Please set your API key or enable local inference."
                  "ragforge set-ollama-api-key <your_api_key>.")