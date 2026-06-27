# Resend Email Setup

Render free web services may not be able to connect to SMTP ports such as 587. Use Resend API email over HTTPS instead.

## 1. Create Resend API Key

1. Open `https://resend.com`.
2. Sign in.
3. Open `API Keys`.
4. Create an API key.
5. Copy the key. Do not commit it to GitHub.

## 2. Add Render Environment Variables

In Render `pawnest-api` > `Environment`, add or update:

```text
EMAIL_DELIVERY_PROVIDER=resend
RESEND_API_KEY=your-resend-api-key
RESEND_FROM_EMAIL=PawNest <onboarding@resend.dev>
CONTRACT_NOTIFICATION_EMAIL=renjiale549@gmail.com
ORDER_NOTIFICATION_EMAIL=renjiale549@gmail.com
SEND_CUSTOMER_ORDER_EMAIL=false
```

For first testing without a domain, `onboarding@resend.dev` is the safest sender. After verifying a real domain in Resend, change `RESEND_FROM_EMAIL` to your domain sender.

## 3. Deploy And Test

Click `Save, rebuild, and deploy` in Render.

After deploy is live, submit a new inquiry from:

```text
https://renjiale549-hash.github.io/pawnest/
```

The response should include:

```json
{
  "email_sent": true
}
```

The inquiry should still appear in Django Admin, and the email should arrive at `CONTRACT_NOTIFICATION_EMAIL`.
