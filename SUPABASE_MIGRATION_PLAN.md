# Supabase Migration Plan - Phase 1

## Overview
Migrate from local JSON storage to Supabase for article storage, while maintaining the beautiful dashboard UI and functionality.

## Current Architecture
- **Storage**: Local JSON files (`.tmp/articles.json`, `.tmp/processed_articles.json`)
- **Dashboard**: Static HTML with JavaScript fetching from local files/API
- **Scrapers**: Python scripts that write to local files

## Target Architecture
- **Storage**: Supabase PostgreSQL database
- **Dashboard**: Static HTML with Supabase JavaScript client
- **Scrapers**: Python scripts that insert/update Supabase
- **Deployment**: Vercel (frontend) + Modal.com (scrapers)

## Phase 1: Supabase Integration

### 1.1 Database Schema Enhancement
**Current Supabase table structure:**
- ✅ `id` (text) - Primary key
- ✅ `title` (text) - Article title
- ✅ `subtitle` (text) - Article subtitle
- ✅ `url` (text) - Article URL
- ✅ `source` (text) - Source (bens_bites, ai_rundown)
- ✅ `published_at` (timestamptz) - Publication date
- ✅ `saved` (boolean) - Saved status
- ✅ `tags` (jsonb) - Article tags
- ✅ `reading_time` (text) - Estimated reading time
- ✅ `score` (integer) - Relevance score
- ✅ `comments` (integer) - Comment count
- ✅ `created_at` (timestamptz) - Record creation
- ✅ `summary` (text) - Article summary
- ✅ `author` (text) - Article author
- ✅ `category` (text) - Article category
- ✅ `image_url` (text) - Article image URL

**RLS Policy:** Already has "Allow anonymous access" policy

### 1.2 Python Scraper Migration
**Changes needed:**
1. Add Supabase client dependency
2. Replace file writing with Supabase operations
3. Implement upsert logic (insert or update based on URL hash)
4. Maintain backward compatibility during transition

### 1.3 Dashboard Frontend Migration
**Changes needed:**
1. Add Supabase JavaScript client
2. Replace fetch('/api/articles') with Supabase queries
3. Keep localStorage for saved articles (no auth needed)
4. Add error handling with fallback

## Implementation Steps

### Step 1: Update Python Scrapers
- Install `supabase-py` dependency
- Modify `tools/scrapers/newsletter_scraper.py` to write to Supabase
- Create Supabase client utility
- Implement upsert logic

### Step 2: Update Dashboard Frontend
- Add Supabase JavaScript client CDN
- Modify `loadArticles()` function
- Update article rendering to use Supabase data structure
- Add error handling and loading states

### Step 3: Test Integration
- Run scraper to populate Supabase
- Test dashboard loading from Supabase
- Verify saved articles functionality
- Test error scenarios

### Step 4: Data Migration
- One-time script to migrate existing articles to Supabase
- Verify data integrity
- Update dashboard to use Supabase as primary source

## Technical Details

### Supabase Client Configuration
**Python (scrapers):**
```python
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
```

**JavaScript (dashboard):**
```javascript
const { createClient } = supabase
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)
```

### Data Transformation
**Current JSON structure:**
```json
{
  "id": "hash",
  "title": "Article Title",
  "source": "bens_bites",
  "url": "https://...",
  "summary": "Article summary",
  "published_at": "2024-01-01T00:00:00Z",
  "category": "AI News",
  "author": "Author Name",
  "image_url": "https://...",
  "is_saved": false
}
```

**Supabase structure:** Maps directly to existing table schema

## Migration Strategy

### Option A: Gradual Migration
1. Keep existing JSON files as backup
2. Run scrapers to populate Supabase
3. Update dashboard to try Supabase first, fallback to JSON
4. Once stable, remove JSON fallback

### Option B: Immediate Cutover
1. Migrate all existing data to Supabase
2. Update scrapers and dashboard simultaneously
3. Deploy new version

**Recommended: Option A** for smoother transition

## Next Phases

### Phase 2: GitHub Repository Setup
- Organize project structure
- Add deployment configurations
- Set up environment variables

### Phase 3: Vercel Deployment
- Configure static site hosting
- Set up environment variables
- Deploy dashboard

### Phase 4: Modal.com Scheduled Scraping
- Containerize scrapers
- Set up 6-hour cron schedule
- Configure error handling

## Success Criteria
- ✅ Articles load from Supabase instead of local files
- ✅ Saved articles functionality preserved
- ✅ Dashboard design and animations intact
- ✅ Error handling with graceful fallbacks
- ✅ Performance comparable to current implementation

## Risk Mitigation
- **Data Loss**: Keep JSON backups during migration
- **Downtime**: Use gradual migration approach
- **Performance**: Test Supabase query performance
- **Errors**: Implement comprehensive error handling