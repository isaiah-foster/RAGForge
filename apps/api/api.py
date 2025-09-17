# 'uvicorn apps.api.api:app --reload' to run

from fastapi import FastAPI
from pydantic import BaseModel
from services.runtimes import llm
from services.retrieval.retrieve import retrieve
from services.retrieval import embed



app = FastAPI()

@app.get("/")
async def root():
    return {"Welcome to RAGForge"}


# Request schema for /chat endpoint
class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_input = request.query.lower()
    return {"response": f"\n AI: {llm.get_response(user_input, retrieve(user_input))}"}