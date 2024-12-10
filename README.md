# Text Transformation Service

This Python-based REST API accepts natural language input and performs various transformations or analyses on the text. Built with a modular architecture, it is designed for extensibility, enabling seamless integration of additional features. The initial implementation includes chunking functionality, providing meaningful text segmentation by preserving sentence boundaries and maintaining semantic coherence.

# Features

1.  Rest API, Built with **Flask** and **Gunicorn** for robust and scalable service deployment.

2.  Text chunking function that splits text into chunks of a given size:

- Preserves sentence boundaries using **NLTK** for accurate filtering and meaningful unit handling.
- Uses **SpaCy** to ensure semantic coherence by generating representations for sentences and measuring their similarities. A 20% buffer allows flexibility in chunk size while grouping semantically related sentences for coherent chunks.

3. A comprehensive test suite is built with pytest, utilizing fixtures to streamline setup and testing. It covers valid inputs, edge cases such as short texts and large chunk sizes, and robust error handling scenarios, including missing or invalid inputs.

# Prerequisites

1. Docker installed on your machine

2. An amd64 architecture is required to run the Docker image.

# How to Run

### Using Docker

This section covers the steps required to get the application up and running using Docker, which ensures that it runs in a consistent environment irrespective of the host system.

#### 1. Pull the Docker Image

First, install Docker if you haven't. [Docker's official website](https://www.docker.com/products/docker-desktop). After installation, pull the Docker image from Docker Hub:

```bash

docker  pull  ajfroster/text_transformation_service:latest

```

The docker hub repository docker hub can found here: https://hub.docker.com/repository/docker/ajfroster/text_transformation_service/general

#### 2. Run the Docker Container

Once the image is downloaded, run it as a container. This makes the application accessible on your local machine

```bash

docker  run  -p  4000:8000  ajfroster/text_transformation_service:latest

```

This command starts the container and maps port `8000`, where Gunicorn hosts the Flask application inside the Docker image, to port `4000` on your host machine. As a result, you can test the service locally by sending requests to `http://localhost:4000`

###### A. Calling API

Here's how [Postman](https://www.postman.com/) can be used to interact with the API:

1. Create a POST request pointed to http://127.0.0.1:4000/chunk

2. In the Header Tab: Key=Content-Type, Value=application/json

3. In the Body Tab: Select "Raw" input and JSON, here is a sample input for the body:

```bash

{ "text":  "Natural language processing is a fascinating field. It involves the interaction between computers and human language.",  "chunk_size":  50  }

```

The resulting output would look like this:

```bash

{"chunks":["Natural language processing is a fascinating field.","It involves the interaction between computers and human language."]}


```

If you don't like postman, here is a sample curl command:

```bash

curl  -X  POST  http://localhost:4000/chunk  -H  "Content-Type: application/json"  -d  "{\"text\": \"Natural language processing is a fascinating field. It involves the interaction between computers and human language.\", \"chunk_size\": 50}"

```

###### B. Test Suite Testing

The Text Transformation Service includes a comprehensive test suite built with pytest. These tests cover a variety of scenarios, including valid inputs, edge cases like short text or large chunk sizes, and error handling for invalid or missing input data. The service’s design and test coverage ensure reliability and robust handling of edge cases.

The tests use pytest fixtures for modular setup. The test_app fixture initializes the Flask app in testing mode, while client simplifies HTTP requests. This approach follows Flask’s testing guidelines, ensuring flexibility for future extensions.

To execute the test suite, use the following command, which runs the tests inside the Docker container:

```bash

docker  run  ajfroster/text_transformation_service:latest  pytest  -v

```

Here are a few highlights of the test cases:

    -Endpoint sanity tests ensure the /chunk endpoint behaves as expected.
    -Valid input tests verify functionality with typical text and chunk size inputs.
    -Semantic similarity tests validate that chunks maintain coherence based on SpaCy’s semantic similarity features.
    -Buffer logic tests confirm that the chunk size flexibility (20% buffer) works correctly.
    -Error handling tests cover scenarios like missing fields, invalid JSON, or empty text.

By running these tests locally or in the container, developers can confidently ensure that the service behaves as expected under various conditions.
