import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarity(df):
    df = df.drop_duplicates(subset=["title"])
    df = df.dropna(subset=["title"])

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["title"])

    similarity_matrix = cosine_similarity(tfidf_matrix)

    results = []
    n = len(df)
    titles = df["title"].tolist()
    sources = df["source"].tolist()

    for i in range(n):
        for j in range(i + 1, n):
            score = round(similarity_matrix[i][j], 3)
            if score > 0.1:
                results.append({
                    "source_a": sources[i],
                    "title_a": titles[i],
                    "source_b": sources[j],
                    "title_b": titles[j],
                    "similarity": score
                })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("similarity", ascending=False)
    return results_df


if __name__ == "__main__":
    df = pd.read_csv("data/processed/news_sentiment.csv")
    results_df = compute_similarity(df)

    print(results_df[["source_a", "source_b", "similarity"]].to_string())

    results_df.to_csv("data/processed/news_similarity.csv", index=False)
    print("\nKaydedildi: data/processed/news_similarity.csv")