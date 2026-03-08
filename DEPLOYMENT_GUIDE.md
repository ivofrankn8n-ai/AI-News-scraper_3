# AI News Dashboard - Deployment Guide

## Phase 1: Supabase Integration ✅ COMPLETED

### What's Ready
- ✅ Supabase client utilities (Python & JavaScript)
- ✅ Updated scrapers with Supabase support
- ✅ Dashboard configured for Supabase fetching
- ✅ Environment variable templates
- ✅ Migration script for existing data
- ✅ Graceful fallback to local storage

### Next Steps Required

## Phase 2: GitHub Repository Setup

### 2.1 Create GitHub Repository
1. Create new repository on GitHub
2. Push your code:
```bash
git init
git add .
git commit -m "Initial commit: AI News Dashboard with Supabase integration"
git branch -M main
git remote add origin https://github.com/yourusername/ai-news-dashboard.git
git push -u origin main
```

### 2.2 Repository Structure
```
AI_NEWS-3/
├── dashboard.html          # Main dashboard
├── serve.py               # Local development server
├── requirements.txt       # Python dependencies
├── .env.template          # Environment variables template
├── tools/                 # Python scripts
│   ├── scrapers/         # Newsletter scrapers
│   ├── processors/       # Data processing
│   ├── storage/          # Storage utilities
│   └── migrate_to_supabase.py  # Data migration
└── docs/                  # Documentation
```

## Phase 3: Vercel Deployment

### 3.1 Deploy to Vercel
1. Connect GitHub repository to Vercel
2. Configure build settings:
   - **Framework Preset**: Other
   - **Build Command**: (leave empty)
   - **Output Directory**: . (current directory)
   - **Install Command**: (leave empty)

### 3.2 Environment Variables
Add these environment variables in Vercel:
```
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
```

### 3.3 Custom Domain (Optional)
- Configure custom domain in Vercel settings
- Update DNS records as instructed

## Phase 4: Modal.com Scheduled Scraping

### 4.1 Modal.com Setup
1. Create account at modal.com
2. Install Modal CLI:
```bash
pip install modal
```

3. Authenticate:
```bash
modal token new
```

### 4.2 Create Scraper Deployment
Create `modal_scraper.py`:
```python
import modal
import os

app = modal.App("ai-news-scraper")

@app.function(
    schedule=modal.Cron("0 */6 * * *"),  # Every 6 hours
    secrets=[
        modal.Secret.from_name("supabase-credentials")
    ]
)
def scrape_articles():
    # Your scraping logic here
    pass
```

### 4.3 Deploy to Modal
```bash
modal deploy modal_scraper.py
```

## Migration Process

### Step 1: Set Up Supabase Credentials
1. Get your Supabase project URL and anon key
2. Add credentials to Vercel environment variables
3. Test connection using the migration script

### Step 2: Migrate Existing Data
```bash
# Set environment variables
export SUPABASE_URL="your-url"
export SUPABASE_ANON_KEY="your-key"

# Run migration
python tools/migrate_to_supabase.py
```

### Step 3: Deploy Dashboard
1. Push code to GitHub
2. Deploy to Vercel
3. Verify dashboard loads articles from Supabase

### Step 4: Set Up Scheduled Scraping
1. Deploy scraper to Modal.com
2. Verify articles are being added to Supabase
3. Monitor scraping logs

## Testing Checklist

### Before Deployment
- [ ] Dashboard loads articles from local JSON files
- [ ] Saved articles functionality works
- [ ] All filters and search work correctly
- [ ] Layout is stable and responsive

### After Supabase Migration
- [ ] Dashboard loads articles from Supabase
- [ ] Fallback to local files works when Supabase unavailable
- [ ] Migration script successfully moves existing data
- [ ] Scrapers can write to Supabase

### After Full Deployment
- [ ] Vercel deployment accessible via URL
- [ ] Modal.com scraper runs on schedule
- [ ] New articles appear in dashboard automatically
- [ ] Performance meets expectations

## Troubleshooting

### Common Issues

**Supabase Connection Fails**
- Verify API key has correct permissions
- Check RLS policies allow public read access
- Test connection with simple REST call

**Dashboard Doesn't Load Articles**
- Check browser console for errors
- Verify Supabase credentials in environment variables
- Test fallback to local files
- **CORS Issues**: Local development may show CORS errors. These will resolve when deployed to Vercel with a proper domain.

**Scraper Fails on Modal**
- Check Modal logs for error messages
- Verify environment variables are set correctly
- Test scraper locally first

## Maintenance

### Regular Tasks
- Monitor scraper performance
- Update dependencies periodically
- Backup Supabase data regularly
- Monitor dashboard performance

### Scaling Considerations
- Add more newsletter sources
- Implement pagination for large article sets
- Add caching for better performance
- Consider CDN for static assets

## Success Metrics

- ✅ Articles load from Supabase instead of local files
- ✅ Dashboard accessible via public URL
- ✅ Scrapers run automatically every 6 hours
- ✅ Performance comparable to local version
- ✅ Graceful error handling for all scenarios

## Next Phase Considerations

### Potential Enhancements
- User authentication for personalized dashboards
- Email notifications for new articles
- Advanced filtering and search
- Mobile app version
- Analytics integration

This completes Phase 1 of the Supabase integration. The foundation is now ready for cloud deployment!