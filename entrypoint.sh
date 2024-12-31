#!/bin/bash

# Start Django server
cd /app/django
python manage.py runserver 0.0.0.0:8000 &
