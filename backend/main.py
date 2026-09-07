from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import chat, voice, session

app = FastAPI(
    title="AI Language Coach API",
    version="0.1.0",
    description="Role 4 backend for frontend, voice, session history, and team integration."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(voice.router)
app.include_router(session.router)


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok",
        "service": "AI Language Coach API"
    }
