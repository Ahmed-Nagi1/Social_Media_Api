# Base image for the environment
FROM python:3.10-slim AS base

# Django setup
WORKDIR /app/django
COPY social_media_api/ /app/django/
RUN pip install --no-cache-dir -r requirements.txt

# Entrypoint script
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose port for the Django service
EXPOSE 8000

# Default command
CMD ["/app/entrypoint.sh"]
