# PostPilot 🚀
**Automated Social Media Bot for Kitwe Small Businesses**

Posts to Facebook, WhatsApp, and Instagram automatically.
Clients control everything by sending WhatsApp messages to the bot.

---

## How it works

1. A client texts your bot's WhatsApp number:
   ```
   POST: New Samsung A15 in stock! K2,800 only. Visit Freedom Way.
   ```
2. The bot replies confirming the scheduled time
3. At the scheduled time, the post goes live on **Facebook + WhatsApp + Instagram** automatically

---

## Client Commands

| Command | Example |
|---|---|
| `POST: <message>` | `POST: 🔥 Weekend sale — 20% off all shoes!` |
| `SCHEDULE: HH:MM \| <message>` | `SCHEDULE: 17:00 \| Closing soon, grab your order!` |
| `STATUS` | Shows upcoming queued posts |
| `CLEAR` | Cancels all queued posts |
| `HELP` | Shows command list |

---

## Setup Guide

### Step 1 — Meta Developer Account
1. Go to https://developers.facebook.com and create an app
2. Add products: **WhatsApp** and **Facebook Login for Business**
3. Note your **App ID** and **App Secret**

### Step 2 — Facebook Page Token
1. In your app dashboard → Tools → Graph API Explorer
2. Select your Page → generate token with:
   - `pages_manage_posts`
   - `pages_read_engagement`
3. **Convert to a never-expiring token** (important!)
4. Copy into `.env` as `FB_PAGE_ACCESS_TOKEN`
5. Copy your Page ID as `FB_PAGE_ID`

### Step 3 — WhatsApp Business API
1. In your Meta app → WhatsApp → API Setup
2. Note the **Phone Number ID** → `WA_PHONE_NUMBER_ID`
3. Generate a **permanent system user token** → `WA_ACCESS_TOKEN`
4. Set your webhook URL (after deploying to Render):
   - URL: `https://your-app.onrender.com/webhook`
   - Verify token: same as `WEBHOOK_VERIFY_TOKEN` in your `.env`
   - Subscribe to: `messages`

### Step 4 — Instagram
1. Your Instagram account must be a **Business or Creator** account
2. Connect it to your Facebook Page (Instagram Settings → Connected Accounts)
3. In Graph API Explorer, call:
   `GET /me/accounts` → find your Page → `GET /{page-id}?fields=instagram_business_account`
4. That gives your `IG_USER_ID`
5. Use the same Page Access Token for `IG_ACCESS_TOKEN`

### Step 5 — Deploy to Render (Free)
```bash
# 1. Push your code to GitHub
git init
git add .
git commit -m "PostPilot bot"
git remote add origin https://github.com/YOUR_USERNAME/postpilot.git
git push -u origin main

# 2. Go to https://render.com → New → Web Service
# 3. Connect your GitHub repo
# 4. Add environment variables from .env.example
# 5. Deploy — your webhook URL will be:
#    https://your-service-name.onrender.com/webhook
```

### Step 6 — Register Webhook with Meta
1. In Meta app dashboard → WhatsApp → Configuration
2. Webhook URL: `https://your-service-name.onrender.com/webhook`
3. Verify token: your `WEBHOOK_VERIFY_TOKEN`
4. Click **Verify and Save**
5. Subscribe to `messages`

---

## Project Structure

```
postpilot/
├── main.py                    # Flask app + webhook endpoints
├── requirements.txt
├── render.yaml                # Render deployment config
├── .env.example               # Copy to .env and fill in
│
├── bot/
│   └── whatsapp_receiver.py   # Parses client commands
│
├── scheduler/
│   ├── queue_manager.py       # SQLite queue (stores/retrieves posts)
│   └── job_runner.py          # Background thread — fires posts every minute
│
└── platforms/
    ├── facebook.py            # Facebook Graph API
    ├── whatsapp.py            # WhatsApp Business Cloud API
    └── instagram.py           # Instagram Graph API
```

---

## Posting Schedule (default)

Posts are auto-assigned to these slots (best times for Zambian audience):
- **08:00** — Morning commute
- **12:30** — Lunch break
- **17:00** — Evening commute
- **19:30** — Prime social time

Edit `DEFAULT_SLOTS` in `scheduler/queue_manager.py` to change these.

---

## Growing the Business

Once running, you can charge clients:
- **K250/month** — 1 platform, 30 posts
- **K550/month** — All 3 platforms, unlimited posts
- **K950/month** — All platforms + custom graphics + priority support

Each new client just needs their phone number registered and their social accounts linked once.
