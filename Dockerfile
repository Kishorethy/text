# Use an official Python image as a base
FROM python:3.10-slim

# Set environment variable to avoid Tkinter crashing in Docker
ENV DISPLAY=:0
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for Tkinter and GUI
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    libgl1-mesa-glx \
    libxrender1 \
    espeak \ 
    libespeak-ng1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Copy requirements.txt to the container
COPY requirements.txt /app/requirements.txt


# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose a port (optional if the application uses one)
EXPOSE 8080

# Command to run your script
CMD ["python3", "text2speech.py"]
