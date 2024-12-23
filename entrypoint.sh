#!/bin/bash

# Start Django server
cd /app/django
python manage.py runserver 0.0.0.0:8000 &

# Start Astro server
cd /app/astro
pnpm run dev --host 0.0.0.0 &

# Wait for all background processes to exit
wait
# uvicorn social_media_api.config.asgi:application