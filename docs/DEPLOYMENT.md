# VPS Deployment Guide

This project is designed for a simple, stable VPS deployment:

- Ubuntu 24.04 LTS
- Nginx
- Gunicorn
- PostgreSQL
- Certbot HTTPS
- Vue built into `frontend/dist`
- Django serving APIs and Admin

## Required Information

Prepare these before production deployment:

- Domain name, for example `example.com` and `www.example.com`
- VPS SSH access
- Production admin email
- SMTP host, port, username, and app password
- PostgreSQL database name, user, and password
- Final business email and WhatsApp/phone for the site
- Real product pricing and whether prices are sample, retail, or inquiry-only

## Server Packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nodejs npm postgresql postgresql-contrib nginx certbot python3-certbot-nginx
```

## Suggested Paths

```text
/var/www/pawnest
/var/www/pawnest/.venv
/var/www/pawnest/staticfiles
/var/www/pawnest/media
/etc/pawnest.env
```

## PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE pawnest;
CREATE USER pawnest_user WITH PASSWORD 'change-me';
GRANT ALL PRIVILEGES ON DATABASE pawnest TO pawnest_user;
\q
```

## Environment File

Create `/etc/pawnest.env`:

```text
SECRET_KEY=change-me-to-a-long-random-production-secret
DEBUG=false
ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
DATABASE_URL=postgres://pawnest_user:change-me@127.0.0.1:5432/pawnest
STATIC_ROOT=/var/www/pawnest/staticfiles
MEDIA_ROOT=/var/www/pawnest/media
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false
EMAIL_HOST_USER=your-sender@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=PawNest <your-sender@gmail.com>
CONTRACT_NOTIFICATION_EMAIL=your-admin@example.com
ORDER_NOTIFICATION_EMAIL=your-admin@example.com
SEND_CUSTOMER_ORDER_EMAIL=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true
SECURE_SSL_REDIRECT=false
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=false
SECURE_HSTS_PRELOAD=false
```

Use a real generated secret and real SMTP app password.

## Application Setup

From `/var/www/pawnest`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd frontend
npm ci
npm run build
cd ..
set -a
. /etc/pawnest.env
set +a
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
```

## Gunicorn systemd Service

Create `/etc/systemd/system/pawnest.service`:

```ini
[Unit]
Description=PawNest Django Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/pawnest
EnvironmentFile=/etc/pawnest.env
ExecStart=/var/www/pawnest/.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8001 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo chown -R www-data:www-data /var/www/pawnest
sudo systemctl daemon-reload
sudo systemctl enable --now pawnest
sudo systemctl status pawnest
```

## Nginx

Create `/etc/nginx/sites-available/pawnest`:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    client_max_body_size 20m;

    location /static/ {
        alias /var/www/pawnest/staticfiles/;
    }

    location /media/ {
        alias /var/www/pawnest/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it:

```bash
sudo ln -s /etc/nginx/sites-available/pawnest /etc/nginx/sites-enabled/pawnest
sudo nginx -t
sudo systemctl reload nginx
```

## HTTPS

```bash
sudo certbot --nginx -d example.com -d www.example.com
```

After HTTPS works, set `SECURE_SSL_REDIRECT=true` in `/etc/pawnest.env` and restart:
If the site is stable on HTTPS, also set `SECURE_HSTS_SECONDS=31536000`. Only enable `SECURE_HSTS_INCLUDE_SUBDOMAINS=true` or `SECURE_HSTS_PRELOAD=true` after confirming all subdomains are HTTPS-ready.

```bash
sudo systemctl restart pawnest
```

## Release Updates

```bash
cd /var/www/pawnest
source .venv/bin/activate
pip install -r requirements.txt
cd frontend
npm ci
npm run build
cd ..
set -a
. /etc/pawnest.env
set +a
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py check --deploy
sudo systemctl restart pawnest
sudo systemctl reload nginx
```

## Verification

- Visit `/`
- Visit `/admin/`
- Submit one inquiry
- Submit one order
- Confirm records in Django Admin
- Confirm admin email notifications arrive

## Backup Notes

Back up PostgreSQL before each major update:

```bash
pg_dump -U pawnest_user -h 127.0.0.1 pawnest > pawnest-backup.sql
```
