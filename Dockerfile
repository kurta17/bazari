# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables to avoid Python buffering and ensure that logs are shown
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the required packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port that your Flask app runs on (this should match the port in your docker-compose.yml)
EXPOSE 8000

# Command to run the app using Gunicorn
CMD ["gunicorn", "-b", ":8000", "app:app"]
