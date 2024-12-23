# Base image for the combined environment
FROM python:3.10-slim AS base

# Install Node.js for Astro
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g pnpm && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Django setup
WORKDIR /app/django
COPY social_media_api/ /app/django/
RUN pip install --no-cache-dir -r requirements.txt

# Astro setup
WORKDIR /app/astro
COPY social_media_ui/ /app/astro/
RUN pnpm install

# Entrypoint script
WORKDIR /app
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose ports for both services
EXPOSE 8000 4321

# Default command
CMD ["/app/entrypoint.sh"]
