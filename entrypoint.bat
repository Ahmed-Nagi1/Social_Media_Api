start "Django" cmd /k ".\.venv\Scripts\activate && python social_media_api/manage.py runserver"
start "Astro" cmd /k "pnpm --prefix ./social_media_ui run dev --host=127.0.0.1"
