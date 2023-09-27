# Use an official Python runtime as a parent image
FROM python:3.11.4-slim

# Set the working directory to /app
WORKDIR /app

# Copy the script files into the container
COPY . /app

COPY /chromedriver-linux64 /app/chromedriver-linux64

# Create the 'profiles' and 'logs' directories inside the container
RUN mkdir -p /app/profiles && mkdir -p /app/error_logs/api_errors && mkdir -p /app/error_logs/app_errors

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt