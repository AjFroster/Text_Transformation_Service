# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the setup script for NLTK
RUN python setup_nlp_resources.py

# Define environment variable
ENV NAME World

# DOCKER RUN

# Run app.py when the container launches
# CMD ["python", "app.py"]
# Use to remove Flask dev warning on run
# CMD ["gunicorn","app:app"]
CMD ["gunicorn","--bind","0.0.0.0:8000","app:app"]