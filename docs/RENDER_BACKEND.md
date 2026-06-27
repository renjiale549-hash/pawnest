# Render Backend Deployment

This file is for the low-cost backend path:

```text
Frontend: GitHub Pages
Backend: Render Web Service
Database: Render PostgreSQL
```

The GitHub Pages frontend is already live at:

```text
https://renjiale549-hash.github.io/pawnest/
```

## What This Enables

- Product API from Django
- Inquiry saving
- Order saving
- Django Admin
- PostgreSQL database

Email notification needs real SMTP variables after the Render service is created.

## Deploy On Render

1. Open Render:

```text
https://dashboard.render.com/
```

2. Sign in with GitHub.
3. Choose `New` > `Blueprint`.
4. Select repository:

```text
renjiale549-hash/pawnest
```

5. Render should detect `render.yaml`.
6. Create the Blueprint.
7. Wait for:
   - `pawnest-db`
   - `pawnest-api`

The backend URL should look like:

```text
https://pawnest-api.onrender.com
```

If Render gives a slightly different URL, use that exact URL.

## Create Admin User On Render

After deployment, open the Render service shell and run:

```bash
python manage.py createsuperuser
```

Then open:

```text
https://YOUR_RENDER_BACKEND/admin/
```

## Connect GitHub Pages To Render Backend

In GitHub:

1. Open `renjiale549-hash/pawnest`.
2. Go to `Settings`.
3. Go to `Secrets and variables`.
4. Go to `Actions`.
5. Open `Variables`.
6. Add repository variable:

```text
Name: VITE_API_BASE_URL
Value: https://YOUR_RENDER_BACKEND
```

Example:

```text
VITE_API_BASE_URL=https://pawnest-api.onrender.com
```

7. Go to `Actions`.
8. Run `Deploy frontend to GitHub Pages` manually, or push a new commit.

After this, the GitHub Pages frontend will call the Render backend for:

```text
/api/products/
/api/contracts/
/api/orders/
/api/newsletter/
```

## SMTP Variables

In Render service environment variables, replace console email with real SMTP when ready:

```text
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false
EMAIL_HOST_USER=your-sender@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=PawNest <your-sender@gmail.com>
CONTRACT_NOTIFICATION_EMAIL=renjiale549@gmail.com
ORDER_NOTIFICATION_EMAIL=renjiale549@gmail.com
SEND_CUSTOMER_ORDER_EMAIL=true
```

Do not put real SMTP passwords in GitHub code.

## Free Tier Notes

Free services can sleep when idle, so the first request may be slow. This is acceptable for early testing, but not ideal for a production store.
