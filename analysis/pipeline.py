import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collector.news_api import fetch_news
from analysis.sentiment import analyze_sentiment
from analysis.similarity import compute_similarity


def run_pipeline(query, page_size=20):
    print(f"[1/3] Haberler çekiliyor: '{query}'...")
    df = fetch_news(query=query, page_size=page_size)
    if df is None or df.empty:
        print("Haber bulunamadı.")
        return
    df.to_csv("data/raw/news_raw.csv", index=False)
    print(f"  {len(df)} haber çekildi.")

    print("[2/3] Sentiment analizi yapılıyor...")
    df = analyze_sentiment(df)
    df.to_csv("data/processed/news_sentiment.csv", index=False)
    pos = (df["sentiment"] == "POSITIVE").sum()
    neg = (df["sentiment"] == "NEGATIVE").sum()
    print(f"  Pozitif: {pos} | Negatif: {neg}")

    print("[3/3] Benzerlik hesaplanıyor...")
    similarity_df = compute_similarity(df)
    similarity_df.to_csv("data/processed/news_similarity.csv", index=False)
    print(f"  {len(similarity_df)} eşleşme bulundu.")

    print("\nPipeline tamamlandı.")
    print("  data/processed/news_sentiment.csv")
    print("  data/processed/news_similarity.csv")


if __name__ == "__main__":
    query = input("Arama konusu: ")
    run_pipeline(query=query, page_size=20)