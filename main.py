from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from model import Recommender
import os

app = FastAPI(title="Movie Recommender API", version="1.0.0")

# Allow local frontends during dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rec = Recommender(os.path.join(os.path.dirname(__file__), "data", "movies.csv"))

class Movie(BaseModel):
    title: str
    genres: str
    overview: str
    year: Optional[int] = None

@app.get("/")
def root():
    return {
        "name": "Movie Recommender API",
        "status": "ok",
        "count": rec.count(),
        "tip": "Try /api/recommend?title=Inception"
    }

@app.get("/api/search")
def search(q: str = Query(..., min_length=1), limit: int = 15):
    results = rec.search(q, limit=limit)
    return {"query": q, "results": results}

@app.get("/api/random")
def random(k: int = 12):
    return {"results": rec.random(k=k)}

@app.get("/api/recommend")
def recommend(title: str, k: int = 10):
    try:
        recs = rec.recommend(title, k=k)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"title": title, "recommendations": recs}