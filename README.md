# AI News Dashboard

A production-ready AI news dashboard that displays articles from Supabase cloud database.

## Live Dashboard

**URL**: https://ai-news-scraper-3.vercel.app

## Features

- **Real-time articles** from Supabase database
- **Today filtering** - shows only today's articles
- **Search & Filter** - filter by source (Ben's Bytes, AI Rundown) or saved articles
- **Save articles** - persists in localStorage
- **Refresh** - manually refresh articles with "Searching Articles" status
- **Responsive** - works on desktop and mobile

## Architecture

```
Browser → Vercel (API Proxy) → Supabase Database
         ↓
      Static HTML/CSS/JS
```

## Project Structure

```
AI_NEWS-3/
├── index.html              # Dashboard frontend
├── api/
│   └── articles.js        # Serverless API proxy
├── vercel.json            # Vercel configuration
├── .env                   # Environment variables
└── *.md                   # Documentation
```

## Development

### Local Development

```bash
# Start local server
python serve.py

# Open http://localhost:8000
```

### Deployment

Changes pushed to GitHub automatically deploy to Vercel.

## API

### GET /api/articles

Returns all articles from Supabase.

**Response:**
```json
{
  "success": true,
  "articles": [...],
  "count": 35
}
```

## Supabase

- **Project**: keajnbcsqgyfgyikvbca.supabase.co
- **Table**: articles
- **Data**: Ben's Bytes + AI Rundown articles

---

Built with vanilla HTML/CSS/JS
