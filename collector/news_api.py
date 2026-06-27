import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(query, sources=None, page_size=20):
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": query,
        "pageSize": page_size,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY,
    }
    
    if sources:
        params["sources"] = ",".join(sources)

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "ok":
        print(f"Hata: {data.get('message')}")
        return None

    articles = data["articles"]
    
    df = pd.DataFrame([{
        "source": a["source"]["name"],
        "title": a["title"],
        "description": a["description"],
        "url": a["url"],
        "published_at": a["publishedAt"],
    } for a in articles])

    return df


if __name__ == "__main__":
    df = fetch_news(query="artificial intelligence", page_size=10)
    print(df[["source", "title"]].to_string())
    
    df.to_csv("data/raw/news_raw.csv", index=False)
    print("\nKaydedildi: data/raw/news_raw.csv")