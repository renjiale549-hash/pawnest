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

For the first version, create the Django Admin user through Render environment variables.

In the `pawnest-api` service:

1. Open `Environment`.
2. Add these variables:

```text
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your-email@example.com
DJANGO_SUPERUSER_PASSWORD=your-strong-password
```

3. Click `Save Changes`.
4. Wait for Render to redeploy, or click `Manual Deploy`.
5. After the deploy is live, open:

```text
https://YOUR_RENDER_BACKEND/admin/
```

6. Log in with the username and password from the variables above.
7. After login works, remove `DJANGO_SUPERUSER_PASSWORD` from Render Environment and redeploy. Keeping the username and email variables is harmless; do not keep the password stored longer than needed.

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

Render free web services can block outbound SMTP ports. Prefer Resend over HTTPS for inquiry and order notification email.

In the `pawnest-api` service environment variables, add:

```text
EMAIL_DELIVERY_PROVIDER=resend
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=PawNest <onboarding@resend.dev>
CONTRACT_NOTIFICATION_EMAIL=renjiale549@gmail.com
ORDER_NOTIFICATION_EMAIL=renjiale549@gmail.com
SEND_CUSTOMER_ORDER_EMAIL=false
```

For the first test without a custom domain, use Resend's test sender:

```text
RESEND_FROM_EMAIL=PawNest <onboarding@resend.dev>
```

After adding a verified domain in Resend, change it to your own sender address, for example:

```text
RESEND_FROM_EMAIL=PawNest <hello@yourdomain.com>
```

Do not put the real Resend API key in GitHub code.

The old SMTP configuration is still supported for VPS or paid hosting that allows SMTP:

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

For Gmail:

- `EMAIL_HOST_USER` is the Gmail address that sends the notification.
- `EMAIL_HOST_PASSWORD` must be a Gmail app password, not the normal Gmail login password.
- `CONTRACT_NOTIFICATION_EMAIL` is the mailbox that receives inquiry notifications. It can be the same Gmail address.

After saving these variables, Render redeploys the service. Submit a new inquiry from GitHub Pages and check:

- The API response should include `email_sent: true`.
- The inquiry should appear in Django Admin.
- The notification email should arrive in `CONTRACT_NOTIFICATION_EMAIL`.

## Free Tier Notes

Free services can sleep when idle, so the first request may be slow. This is acceptable for early testing, but not ideal for a production store.
