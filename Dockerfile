# Use Python image as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install the dependencies (required libraries)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . /app/

# Expose port 8000 to be used by Django
EXPOSE 8000

# Set the default command to run Django's development server
ENTRYPOINT ["entrypoint.sh"]