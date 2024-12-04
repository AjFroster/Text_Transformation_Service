import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

# Test Cases

def test_basic_functionality():
    response = requests.post(
        f"{BASE_URL}/chunk",
        json={
            "text":"Natural language processing is a fascinating field. It involves the interaction between computers and human language.",
            "chunk_size": 50
        }
    )
    # print("Response JSON:", response.json())
    # print("Expected:", {
    #     "chunks": [
    #         "Natural language processing is a fascinating field.",
    #         "It involves the interaction between computers and human language."
    #     ]
    # })
    assert response.status_code == 200
    assert response.json() == {
        "chunks": [
            "Natural language processing is a fascinating field.",
            "It involves the interaction between computers and human language."
        ]
    }

def test_short_text():
    response = requests.post(
        f"{BASE_URL}/chunk",
        json={
            "text": "Short sentence.",
            "chunk_size": 50
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "chunks": ["Short sentence."]
    }

def test_large_chunk_size():
    response = requests.post(
        f"{BASE_URL}/chunk",
        json={
            "text": "This is a test sentence. It has multiple sentences to test chunking.",
            "chunk_size": 500
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "chunks": ["This is a test sentence. It has multiple sentences to test chunking."]
    }

def test_missing_field():
    response = requests.post(
        f"{BASE_URL}/chunk",
        json={"chunk_size": 50}
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "Missing 'text' or 'chunk_size' in request body"
    }

def test_invalid_chunk_size():
    response = requests.post(
        f"{BASE_URL}/chunk",
        json={
            "text": "This is a test sentence.",
            "chunk_size": -10
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "Chunk size must be a positive integer."
    }

def test_invalid_json():
    response = requests.post(
        f"{BASE_URL}/chunk",
        data="This is not JSON format."
    )
    
    # Flask return 415 invalid request body or header missing
    assert response.status_code == 415  

def test_empty_text():
    response = requests.post(
        f"{BASE_URL}/chunk",
        json={
            "text": "",
            "chunk_size": 50
        }
    )
    assert response.status_code == 400
    assert response.json() == {
        "error": "Text cannot be empty."
    }

def test_large_input_text():
    large_text = "Sentence one. " + "Sentence two. " * 1000
    response = requests.post(
        f"{BASE_URL}/chunk",
        json={
            "text": large_text,
            "chunk_size": 100
        }
    )
    assert response.status_code == 200
    assert len(response.json()["chunks"]) > 0
    