# Inquiry Email Notification Setup

The contact inquiry API now saves the inquiry to the `contract` table and sends an email notification.

Recipient email:

```text
renjiale549@gmail.com
```

## Local Development

By default, Django uses the console email backend:

```python
django.core.mail.backends.console.EmailBackend
```

This means local submissions will print the email content in the Django server terminal instead of sending a real email.
For inquiry notifications, the API reports `email_sent: false` while this console backend is active, because no real email leaves the server.

## Real SMTP Sending

The project automatically loads email settings from a root `.env` file.

Copy `.env.example` to `.env`, then fill in the sender mailbox and app password:

```powershell
Copy-Item .env.example .env
notepad .env
```

Example `.env` values:

```text
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_USE_SSL=false
EMAIL_HOST_USER=your-sender@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=PawNest <your-sender@gmail.com>
CONTRACT_NOTIFICATION_EMAIL=renjiale549@gmail.com
```

Restart Django after editing `.env`:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

For Gmail, `EMAIL_HOST_PASSWORD` should be an app password, not the normal account login password.

You can test SMTP without submitting the website form:

```powershell
.\.venv\Scripts\python.exe manage.py send_test_inquiry_email
```

This command only succeeds when a real sending backend, or a test email backend, is configured. With the default console backend, it intentionally fails because no real email is delivered.

## Behavior

- If the database save succeeds and email sending succeeds, the API returns `email_sent: true`.
- If the database save succeeds but email sending fails, the inquiry is still saved and the API returns `email_sent: false`.
- Email failures are logged on the Django server side.

## API

Existing endpoint:

```text
POST /api/contracts/
```

Successful response example:

```json
{
  "message": "Submitted successfully.",
  "id": 1,
  "email_sent": true
}
```
