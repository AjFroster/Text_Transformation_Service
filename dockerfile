# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the setup script for NLTK
RUN python setup_nltk.py

# Define environment variable
ENV NAME World

# DOCKER RUN

# Run app.py when the container launches
# CMD ["python", "app.py"]
# Use to remove Flask dev warning on run
CMD ["gunicorn","app:app"]