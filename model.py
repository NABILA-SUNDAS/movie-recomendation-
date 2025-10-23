import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re, random

class Recommender:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        # Clean NaNs
        for col in ["title", "genres", "overview"]:
            self.df[col] = self.df[col].fillna("")
        # Build a simple "document" = overview + genres tokens
        self.df["doc"] = (
            self.df["overview"].astype(str).str.lower() + " " +
            self.df["genres"].astype(str).str.lower().str.replace("|", " ", regex=False)
        )
        # Vectorize
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1,2))
        self.X = self.vectorizer.fit_transform(self.df["doc"].values)
        # Map title -> index (case-insensitive)
        self.title_to_idx = {t.lower(): i for i, t in enumerate(self.df["title"].astype(str))}

    def count(self) -> int:
        return int(self.df.shape[0])

    def _normalize(self, s: str) -> str:
        return re.sub(r"\s+", " ", s.strip().lower())

    def search(self, q: str, limit: int = 15):
        qn = self._normalize(q)
        # simple contains on title; could be improved with fuzzy matching
        mask = self.df["title"].str.lower().str.contains(qn, na=False)
        found = self.df[mask].head(limit)[["title", "genres", "overview", "year"]]
        return found.to_dict(orient="records")

    def random(self, k: int = 12):
        take = self.df.sample(n=min(k, len(self.df)), random_state=None)[["title","genres","overview","year"]]
        return take.to_dict(orient="records")

    def recommend(self, title: str, k: int = 10):
        key = title.lower()
        if key not in self.title_to_idx:
            # try partial match
            candidates = self.df[self.df["title"].str.lower().str.contains(key, na=False)]
            if candidates.empty:
                raise ValueError(f"Title '{title}' not found. Try /api/search?q={title}")
            idx = candidates.index[0]
        else:
            idx = self.title_to_idx[key]

        vec = self.X.getrow(idx)
        sims = cosine_similarity(vec, self.X).ravel()
        # Exclude the same movie
        sims[idx] = -1
        top_idx = sims.argsort()[::-1][:k]
        cols = ["title", "genres", "overview", "year"]
        results = self.df.iloc[top_idx][cols].copy()
        results["score"] = sims[top_idx]
        return results.to_dict(orient="records")