# SMTP Quick Start

The project now loads email settings from a root `.env` file automatically.

## 1. Create `.env`

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and fill in the real sender mailbox:

```text
EMAIL_HOST_USER=your-sender@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=PawNest <your-sender@gmail.com>
CONTRACT_NOTIFICATION_EMAIL=renjiale549@gmail.com
```

For Gmail, `EMAIL_HOST_PASSWORD` must be a Gmail app password, not the normal login password.

## 2. Restart Django

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

## 3. Test From Website

Open:

```text
http://127.0.0.1:8000/
```

Submit the contact inquiry form. The API will:

1. Save the inquiry to the SQLite `contract` table.
2. Send a notification email to `renjiale549@gmail.com`.
3. Return `email_sent: true` when SMTP sending succeeds.

If SMTP sending fails, the inquiry is still saved and the API returns `email_sent: false`.
