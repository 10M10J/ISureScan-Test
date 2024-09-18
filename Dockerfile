# Use the official Python image as the base image
FROM python:3.9-slim

ARG API_KEY
ENV GOOGLE_API_KEY=${API_KEY}
# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask app files into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 8080

# Define the command to run your application
CMD ["python3", "app.py"]
