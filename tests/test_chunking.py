import pytest

# BASE_URL = "http://127.0.0.1:5000"

# Docker image url
# BASE_URL = "http://host.docker.internal:4000"

# Testing Flask Applications Docs: https://flask.palletsprojects.com/en/stable/testing/
from app import app

@pytest.fixture()
def test_app():
    app.config.update({
        "TESTING": True, # Enables testing mode
    })
    yield app # Use app in tests

@pytest.fixture()
def client(test_app):
    return test_app.test_client() # Test Client used for HTTP requests in tests

# Test Cases
def test_chunk_endpoint(client):
    response = client.post(
        f"/chunk",
        json={
            "text": "Natural language processing is a fascinating field. It involves the interaction between computers and human language.",
            "chunk_size": 50,
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "chunks": [
            "Natural language processing is a fascinating field.",
            "It involves the interaction between computers and human language.",
        ]
    }


def test_short_text(client):
    response = client.post(
        f"/chunk", json={"text": "Short sentence.", "chunk_size": 50}
    )
    assert response.status_code == 200
    assert response.get_json() == {"chunks": ["Short sentence."]}


def test_large_chunk_size(client):
    response = client.post(
        f"/chunk",
        json={
            "text": "This is a test sentence. It has multiple sentences to test chunking.",
            "chunk_size": 500,
        },
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "chunks": [
            "This is a test sentence. It has multiple sentences to test chunking."
        ]
    }
    

def test_semantic_similarity_grouping(client):
    response = client.post(
        f"/chunk",
        json={
            "text": "Alice loves programming. She spends hours coding. Her dedication inspires others. Bob likes cooking. He tries new recipes every day.",
            "chunk_size": 80
        }
    )
    print(response.get_json())
    assert response.status_code == 200
    assert response.get_json() == {
        "chunks": [
            "Alice loves programming. She spends hours coding. Her dedication inspires others.",
            "Bob likes cooking. He tries new recipes every day."
        ]
    }

def test_buffer_usage(client):
    response = client.post(
        f"/chunk",
        json={
            "text": "The weather is beautiful today. It makes me want to go outside. The sun is shining brightly. It's a perfect day for a walk in the park.",
            "chunk_size": 70
        }
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "chunks": [
            "The weather is beautiful today. It makes me want to go outside.",
            "The sun is shining brightly. It's a perfect day for a walk in the park."
        ]
    }


def test_semantics_with_topics(client):
    response = client.post(
        f"/chunk",
        json={
            "text": "Python is a popular programming language. It's used for data analysis and machine learning. Hockey is a beloved sport worldwide. I watch it on weekends.",
            "chunk_size": 90
        }

    )
    print(response.get_json())
    assert response.status_code == 200
    assert response.get_json() == {
        "chunks": [
            "Python is a popular programming language. It's used for data analysis and machine learning.",
            "Hockey is a beloved sport worldwide. I watch it on weekends."
        ]
    }


def test_small_chunk_size(client):
    response = client.post(
        f"/chunk",
        json={
            "text": "Short sentences can still cause issues if chunk size is too small. Test cases like this are important.",
            "chunk_size": 30
        }
    )
    assert response.status_code == 200
    assert response.get_json() == {
        "chunks": [
            "Short sentences can still cause issues if chunk size is too small.",
            "Test cases like this are important."
        ]
    }


def test_missing_field(client):
    response = client.post(f"/chunk", json={"chunk_size": 50})
    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Missing 'text' or 'chunk_size' in request body"
    }


def test_invalid_chunk_size(client):
    response = client.post(
        f"/chunk",
        json={"text": "This is a test sentence.", "chunk_size": -10},
    )
    assert response.status_code == 400
    assert response.get_json() == {"error": "Chunk size must be a positive integer."}


def test_invalid_json(client):
    response = client.post(f"/chunk", data="This is not JSON format.")

    # Flask return 415 invalid request body or header missing
    assert response.status_code == 415


def test_empty_text(client):
    response = client.post(f"/chunk", json={"text": "", "chunk_size": 50})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Text cannot be empty."}


def test_large_input_text(client):
    large_text = "Sentence one. " + "Sentence two. " * 1000
    response = client.post(
        f"/chunk", json={"text": large_text, "chunk_size": 100}
    )
    assert response.status_code == 200
    assert len(response.get_json()["chunks"]) > 0
