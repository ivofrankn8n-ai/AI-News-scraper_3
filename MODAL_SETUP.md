# Modal.com Setup Guide

This guide walks you through setting up automated scraping on Modal.com to run every 3 hours.

## Prerequisites

- Modal.com account (you have this)
- Supabase service key (I'll guide you to get this)

---

## Step 1: Get Supabase Service Key

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project: `keajnbcsqgyfgyikvbca`
3. Click **Settings** (gear icon) → **API**
4. Under **Service Role Keys**, click **Copy** on the `service_role` key
5. **Important**: This key has full write access - keep it secure!

---

## Step 2: Install Modal CLI

Open your terminal and run:

```bash
pip install modal
```

---

## Step 3: Login to Modal

```bash
modal token new
```

This will open a browser window. Log in with your Modal.com account and authorize the CLI.

---

## Step 4: Add Secrets to Modal

You need to add your Supabase credentials as secrets:

1. Go to [Modal Dashboard](https://modal.com/secrets)
2. Click **New Secret**
3. Fill in:
   - **Name**: `ai-news-scraper`
   - **Key-value pairs**:
     - `SUPABASE_URL` = `https://keajnbcsqgyfgyikvbca.supabase.co`
     - `SUPABASE_SERVICE_KEY` = `[paste your service_role key here]`
4. Click **Create Secret**

---

## Step 5: Deploy the Scraper

From your project directory:

```bash
cd C:\Users\ers\Portfolio\AI_NEWS-3
modal deploy modal_scraper.py
```

You should see output like:
```
✓ App deployed as 'ai-news-scraper'
```

---

## Step 6: Verify It's Working

1. Go to [Modal Dashboard](https://modal.com/dashboard)
2. Click on your app (`ai-news-scraper`)
3. You should see the function listed with **Cron: 0 */3 * * *** (every 3 hours)
4. Click **Run** to test it manually

---

## How It Works

- **Schedule**: Runs every 3 hours (at 0, 3, 6, 9, 12, 15, 18, 21 UTC)
- **Sources**: Scrapes Ben's Bytes (RSS) and AI Rundown (sitemap)
- **Filtering**: Only uploads articles from today
- **Updates**: 
  - Adds new articles to Supabase
  - Updates `last_scraped_at` timestamp in database
  - Dashboard automatically shows new timestamp

---

## Testing the Dashboard

After deploying to Modal:

1. Wait for the first scrape (or run manually)
2. Visit: https://ai-news-scraper-3.vercel.app
3. The "Last Updated" should show the actual scrape time (e.g., "15:30 UTC")
4. Articles from today will appear in the "New Today" count

---

## Troubleshooting

### Scraper not running?
- Check Modal dashboard for any error logs
- Verify secrets are correctly set

### No articles showing?
- Run the scraper manually from Modal dashboard
- Check Supabase database for new records

### Questions?
Check the Modal docs: https://modal.com/docs
