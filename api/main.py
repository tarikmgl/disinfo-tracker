from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analysis.pipeline import run_pipeline

app = FastAPI(title="Disinfo Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "message": "Disinfo Tracker API çalışıyor"}


@app.get("/analyze")
def analyze(query: str = Query(..., description="Arama konusu")):
    run_pipeline(query=query, page_size=20)
    return {"status": "ok", "query": query}


@app.get("/sentiment")
def sentiment():
    path = "data/processed/news_sentiment.csv"
    if not os.path.exists(path):
        return {"error": "Önce /analyze endpoint'ini çalıştır"}
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


@app.get("/similarity")
def similarity():
    path = "data/processed/news_similarity.csv"
    if not os.path.exists(path):
        return {"error": "Önce /analyze endpoint'ini çalıştır"}
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


@app.get("/summary")
def summary():
    path = "data/processed/news_sentiment.csv"
    if not os.path.exists(path):
        return {"error": "Önce /analyze endpoint'ini çalıştır"}
    df = pd.read_csv(path)
    total = len(df)
    positive = int((df["sentiment"] == "POSITIVE").sum())
    negative = int((df["sentiment"] == "NEGATIVE").sum())
    sources = df["source"].unique().tolist()
    return {
        "total": total,
        "positive": positive,
        "negative": negative,
        "sources": sources
    }