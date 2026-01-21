# 'uvicorn apps.api.api:app --reload' to run
import shutil
from fastapi import FastAPI,UploadFile,File
from pydantic import BaseModel
from server import inference
from server import embedding
from fastapi.responses import StreamingResponse
from core.paths import DATASET_PATH
import asyncio

class API:

    def __init__(self):
     self.app = FastAPI()
     self._setup_routes()
     
    def _setup_routes(self):
        @self.app.get("/")
        async def root():
            return {"Welcome to RAGForge"}

        # Request schema for /chat endpoint
        class ChatRequest(BaseModel):
            query: str

        @self.app.post("/chat")
        async def chat_endpoint(request: ChatRequest):
            user_input = request.query.lower()
            async def gen():
                for chunk in inference.stream_response(user_input, user_input):
                    yield chunk
                    await asyncio.sleep(0)  # allows flush

            return StreamingResponse(
                gen(),
                media_type="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )

        #ISSUE: add db commands to other endpoints
        @self.app.post("/embed")
        async def embed_endpoint():
            return StreamingResponse(
                embedding.embed_docs(),
                media_type="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "X-Accel-Buffering": "no",
                },
            )

        @self.app.post("/upload")
        async def upload(
            files: list[UploadFile] = File(...),          # 1..N
        ):
            UPLOAD_DIR = DATASET_PATH
            saved = []
            for f in files:
                dest = UPLOAD_DIR / f.filename
                dest.parent.mkdir(parents=True, exist_ok=True)

                # stream to disk
                with dest.open("wb") as out:
                    shutil.copyfileobj(f.file, out)

                saved.append(str(dest))

            return {"count": len(saved), "saved": saved}
        
app = API().app