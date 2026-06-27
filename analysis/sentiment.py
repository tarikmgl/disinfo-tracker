import pandas as pd
from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def analyze_sentiment(df):
    titles = df["title"].fillna("").tolist()
    
    results = sentiment_model(titles, truncation=True, max_length=512)
    
    df["sentiment"] = [r["label"] for r in results]
    df["sentiment_score"] = [round(r["score"], 3) for r in results]
    
    return df


if __name__ == "__main__":
    df = pd.read_csv("data/raw/news_raw.csv")
    df = analyze_sentiment(df)
    
    print(df[["source", "title", "sentiment", "sentiment_score"]].to_string())
    
    df.to_csv("data/processed/news_sentiment.csv", index=False)
    print("\nKaydedildi: data/processed/news_sentiment.csv")