import feedparser
import pandas as pd
from sentence_transformers import SentenceTransformer


class RSSLoader:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def fetch_rss_data(self, rss_urls):
        """Fetches and parses RSS feeds."""
        articles = []
        for url in rss_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                articles.append(
                    {
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", ""),
                        "author": entry.get("author", "Unknown"),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                    }
                )
        return pd.DataFrame(articles)

    def generate_embeddings(self, df):
        """Generates embeddings for the provided DataFrame."""
        df["embedding"] = df["summary"].apply(lambda x: self.model.encode(x).tolist())

        print(df.head())
        return df

    def process_rss_feeds(self, rss_urls):
        """Fetches RSS data, processes it, and generates embeddings."""
        df = self.fetch_rss_data(rss_urls)
        if df.empty:
            return df
        return self.generate_embeddings(df)
