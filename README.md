# Text Transformation Service

This is a Python-based REST API that accepts natural language input and performs various transformations or analyses on the text. It includes a chunking functionality as its initial feature.

# Features

1. Rest API built with Flask
2. Text chunking function that splits text into chunks of a given size while preserving sentence boudaries using nltk
3. Comprehensive test cases using pytest

# Prerequisites

1. Docker installed on your machine
2. An amd64 architecture is required to runt he Docker image.

# How to Run

### Using Docker

This section covers the steps required to get the application up and running using Docker, which ensures that it runs in a consistent environment irrespective of the host system.

#### 1. Pull the Docker Image

First, install Docker if you haven't. [Docker's official website](https://www.docker.com/products/docker-desktop). After installation, pull the Docker image from Docker Hub:

```bash
docker pull ajfroster/text_transformation_service:latest
```

The repository can found here: https://hub.docker.com/repository/docker/ajfroster/text_transformation_service/general

#### 2. Run the Docker Container

Once the image is downloaded, run it as a container. This makes the application accessible on your local machine

```bash
docker run -p 4000:80 ajfroster/text_transformation_service:latest
```

This starts the container and maps port 80 of the container to port 4000 on your host machine. This allows the application accessible via: http//localhost:4000

###### A. Manual Testing

Here's how [Postman](https://www.postman.com/) can be used to interact with the API:

1. Create a POST request pointed to http://127.0.0.1:4000/chunk
2. In the Header Tab: Key=Content-Type, Value=application/json
3. In the Body Tab: Select "Raw" input and JSON, here is a sample input for the body:

```bash
{ "text": "Natural language processing is a fascinating field. It involves the interaction between computers and human language.", "chunk_size": 50 }
```

If you don't like postman, here is a sample curl command:

```bash
curl -X POST http://localhost:4000/chunk -H "Content-Type: application/json" -d "{\"text\": \"Natural language processing is a fascinating field. It involves the interaction between computers and human language.\", \"chunk_size\": 50}"
```

###### B. Test Suite Testing

I have created a test suite to cover various scenarios, including:

1. Basic proper input
2. Short text input
3. Large chunk_size (500 characters)
4. Sentence prioritizing for chunk size test 1
5. Sentence prioritizing for chunk size test 2
6. Missing field (json input does not include "text" field)
7. Invalid chunk_size (<= 0)
8. Test Invalid input (not JSON)
9. Text value is empty
10. Large input Text

To run the pytest suite use the command:

```bash
docker run ajfroster/text_transformation_service:latest pytest -v
```
