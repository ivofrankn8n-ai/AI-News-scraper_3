# Deployment Status

## Status: PRODUCTION-READY

**Live Dashboard**: https://ai-news-scraper-3.vercel.app

---

## Features

### Core Functionality
- Articles loaded from Supabase via serverless API proxy
- "Today" count filters to current calendar day only
- Refresh button shows "Searching Articles" status
- "Last Updated" timestamp only changes on manual refresh
- Search and filter by source (Ben's Bytes, AI Rundown, Saved)
- Save articles to localStorage

### Technical Implementation
- Serverless API proxy (`api/articles.js`) solves CORB issues
- Vercel static build for frontend, Node.js for API
- Direct Supabase connection server-side (no client-side CORS)
- Cache disabled for fresh content

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Browser       │────▶│  Vercel         │────▶│  Supabase       │
│  (Dashboard)    │     │  API Proxy      │     │  Database       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  HTML/CSS/JS    │     │  Node.js        │
│  (Static Build) │     │  (Serverless)   │
└─────────────────┘     └─────────────────┘
```

---

## API Endpoint

- **URL**: `https://ai-news-scraper-3.vercel.app/api/articles`
- **Method**: GET
- **Response**: JSON with articles array

---

## Supabase Connection

- **Project**: keajnbcsqgyfgyikvbca.supabase.co
- **Table**: articles
- **RLS Policy**: Public read access enabled

---

## Resources

- **Dashboard**: https://ai-news-scraper-3.vercel.app
- **GitHub**: https://github.com/ivofrankn8n-ai/AI-News-scraper_3.git
- **Vercel**: https://vercel.com/dashboard
- **Supabase**: https://supabase.com/dashboard/project/keajnbcsqgyfgyikvbca
