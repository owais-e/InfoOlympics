# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory in the container
WORKDIR /olympics_app

# Copy the requirements file into the container at /app
COPY requirements.txt /olympics_app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /olympics_app/

# Expose the port that the app will run on (change it if needed)
EXPOSE 8501

# Define environment variable
ENV STREAMLIT_SERVER_PORT=8501

# Define the command to run your Streamlit app
CMD ["streamlit", "run", "app.py"]
