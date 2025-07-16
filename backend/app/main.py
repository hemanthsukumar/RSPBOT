# backend/app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Literal
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.predictor import get_bot_move  # Uses advanced predictor logic

load_dotenv()

# === Initialize FastAPI app ===
app = FastAPI(title="Rock-Paper-Scissors AI Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Request & Response Models ===

class MoveRequest(BaseModel):
    history: List[Literal["rock", "paper", "scissors"]]

class MoveResponse(BaseModel):
    bot_move: Literal["rock", "paper", "scissors"]
    confidence: float
    strategy: str  # "q_table", "ngram", or "random"

# === Endpoints ===

@app.get("/ping")
def ping():
    return {"message": "Bot is alive!"}

@app.post("/move", response_model=MoveResponse)
def move(request: MoveRequest):
    print(f"[INFO] Received user history: {request.history}")
    result = get_bot_move(request.history)
    return result