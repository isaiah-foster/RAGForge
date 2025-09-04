# 'uvicorn apps.api.api:app --reload' to run


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"Welcome to RAGForge"}


# Request schema for /chat endpoint
class ChatRequest(BaseModel):
    query: str

botName = "gpt-oss:20b"

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    return {"response": f"\n{botName}: {request.query}"}