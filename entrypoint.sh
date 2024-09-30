python manage.py makemigrations
python manage.py migrate
uvicorn social_media_api.config.asgi:application