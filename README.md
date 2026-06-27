# PawNest Pet Supplies Independent Store

Django + Vue independent-store prototype for pet lifestyle goods.

## Local Development

Run Django:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Build Vue:

```powershell
cd frontend
npm run build
```

Useful checks:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test core
```

## Core Features

- Product catalog API: `GET /api/products/`, `GET /api/products/<slug>/`
- Inquiry API: `POST /api/contracts/`
- Newsletter API: `POST /api/newsletter/`
- Manual-confirmation order API: `POST /api/orders/`
- Django Admin: `/admin/`

## Deployment

Use `docs/DEPLOYMENT.md` for the VPS + Nginx + Gunicorn + PostgreSQL deployment plan.

For a free frontend-only preview on GitHub Pages, use `docs/GITHUB_PAGES.md`.

For the GitHub Pages frontend plus Render backend path, use `docs/RENDER_BACKEND.md`.
