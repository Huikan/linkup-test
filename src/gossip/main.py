import click
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest

from gossip.rss_loader import RSSLoader

# Initialize Qdrant client
qdrant_client = QdrantClient(url="http://qdrant:6333")


# RSS feeds to fetch
RSS_FEEDS = [
    "https://www.public.fr/people/feed",
    "https://www.public.fr/feed",
    "https://www.public.fr/royautes/feed",
]

# Initialize RSSLoader
loader = RSSLoader()


@click.group()
def cli():
    pass


@cli.command()
def init():
    """Initialize the database."""
    qdrant_client.recreate_collection(
        collection_name="gossip",
        vectors_config={
            "content": rest.VectorParams(distance=rest.Distance.COSINE, size=384)
        },
    )
    click.echo("Database initialized.")


@cli.command()
def load_rss():
    """Fetch and load RSS data into the database."""
    df = loader.process_rss_feeds(RSS_FEEDS)

    if df.empty:
        click.echo("No new articles found.")
        return

    points = [
        {
            "id": index,
            "vector": {"content": row["embedding"]},
            "payload": {
                "title": row["title"],
                "author": row.get("author", "Unknown"),
                "published": row.get("published", "Unknown"),
                "link": row.get("link", ""),
                "summary": row.get("summary", ""),
            },
        }
        for index, row in df.iterrows()
    ]

    # Insert into Qdrant
    qdrant_client.upsert(
        collection_name="gossip",
        points=points,
    )
    click.echo(f"Loaded {len(points)} articles into Qdrant.")
    click.echo("RSS data loaded successfully.")


if __name__ == "__main__":
    cli()
