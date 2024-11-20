import feedparser
import numpy as np
from flask import Flask, render_template, request
from qdrant_client import QdrantClient

from gossip.rss_loader import RSSLoader

app = Flask(__name__)
loader = RSSLoader()
qdrant_client = QdrantClient(url="http://qdrant:6333")
COLLECTION_NAME = "gossip"


@app.route("/")
def index():
    """Serve the front-end HTML."""
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    """Handle query requests and return results."""
    data = request.json
    query_text = data.get("query")
    top_k = 5
    print("query_text:", query_text)
    # Generate query embedding
    query_embedding = loader.model.encode(query_text).tolist()
    print("query_embedding:", query_embedding)
    results = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=("content", query_embedding),
        limit=top_k,
        query_filter=None,
    )

    # Format the results
    formatted_results = [
        {
            "title": result.payload["title"],
            "summary": result.payload["summary"],
            "link": result.payload["link"],
            "similarity": result.score,
        }
        for result in results
    ]
    return {"results": formatted_results}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
