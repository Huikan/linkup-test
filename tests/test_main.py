import pandas as pd
import pytest
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from gossip.app import app, loader

COLLECTION_NAME = "unittest"


@pytest.fixture
def qdrant_client():
    client = QdrantClient(url="http://qdrant:6333")
    yield client
    client.delete_collection(collection_name=COLLECTION_NAME)


@pytest.fixture
def setup_database(qdrant_client):
    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={"content": VectorParams(size=384, distance=Distance.COSINE)},
    )


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the index page."""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Query Interface" in rv.data


def test_query(client, qdrant_client, setup_database):
    """Test the query endpoint."""
    # Insert a test point into Qdrant
    test_point = PointStruct(
        id=1,
        vector={"content": loader.model.encode("this is a unit test").tolist()},
        payload={
            "title": "Test Title",
            "summary": "Test Summary",
            "link": "http://example.com",
        },
    )
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=[test_point])

    # Perform a query
    rv = client.post("/query", json={"query": "Test", "top_k": 1})
    assert rv.status_code == 200
    response_data = rv.get_json()
    assert len(response_data["results"]) == 1
    assert response_data["results"][0]["title"] == "Test Title"
    assert response_data["results"][0]["summary"] == "Test Summary"
    assert response_data["results"][0]["link"] == "http://example.com"
