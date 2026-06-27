# Agent Notes

## Project Overview

This project is a Django + Vue website.

- Backend: Django 4.2.30
- Admin UI: django-simpleui
- Frontend: Vue 3 + Vite
- Database: SQLite, `db.sqlite3`
- Django project package: `config`
- Django app: `core`
- Vue app: `frontend`

## Local Paths

- Project root: `C:\Users\Le\Documents\跟着B站做网站`
- Python virtual environment: `.venv`
- Vue source: `frontend\src`
- Vue production build: `frontend\dist`

## Run Backend

From the project root:

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver 127.0.0.1:8000
```

Main URLs:

- Frontend page: `http://127.0.0.1:8000/`
- Django admin: `http://127.0.0.1:8000/admin/`

## Admin Account

- Username: `admin`
- Email: `renjiale549@gmail.com`
- Nickname stored in `first_name`: `admin`

## Frontend Workflow

Vue is used for the public frontend. Django serves the built Vue files.

After changing Vue files, rebuild from `frontend`:

```powershell
npm run build
```

Then refresh `http://127.0.0.1:8000/`.

## Django Integration Notes

- `config\urls.py` maps `/` to `core.views.frontend`.
- `core\views.py` renders `index.html`.
- `config\settings.py` includes:
  - `simpleui` before `django.contrib.admin`
  - `LANGUAGE_CODE = 'zh-hans'`
  - `TIME_ZONE = 'Asia/Shanghai'`
  - `TEMPLATES['DIRS']` pointing to `frontend\dist`
  - `STATICFILES_DIRS` pointing to `frontend\dist`
- `frontend\vite.config.js` uses `base: '/static/'` so Django can serve built assets.

## Verification Commands

Run these after backend or settings changes:

```powershell
.\.venv\Scripts\python.exe manage.py check
```

Run this after frontend changes:

```powershell
cd frontend
npm run build
```

## Working Guidelines

- Keep the Django admin working at `/admin/`.
- Do not replace the existing Vue/Django setup unless explicitly requested.
- Do not delete `.venv`, `db.sqlite3`, or `frontend\node_modules` unless the user explicitly asks.
- Avoid moving npm or Python cache directories without first checking their size and asking for confirmation.
