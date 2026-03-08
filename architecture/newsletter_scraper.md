# Newsletter Scraper Architecture

## Goal
Extract latest AI articles from newsletter sources and prepare data for dashboard

## Input Sources
1. **Ben's Bytes** (Substack)
   - RSS Feed: https://bensbites.substack.com/feed
   - Format: XML/RSS

2. **The AI Rundown** (Beehiiv) 
   - Article URLs: Individual post URLs from sitemap
   - Format: HTML scraping

## Data Processing Pipeline

### Phase 1: Data Collection
```python
# tools/scrapers/newsletter_scraper.py
- Fetch RSS feed (Ben's Bytes)
- Parse XML to extract article metadata
- Fetch individual article pages (The AI Rundown) 
- Extract content via HTML parsing
```

### Phase 2: Data Transformation
```python
# tools/processors/data_processor.py
- Normalize data structure
- Extract key fields: title, content, published_date, source
- Filter articles from last 24 hours
- Generate unique IDs
```

### Phase 3: Storage
```python
# tools/storage/local_storage.py
- Save to .tmp/articles.json
- Maintain article history
- Track saved articles
```

## Article Schema
```json
{
  "id": "unique_hash",
  "title": "string",
  "source": "bens_bites|ai_rundown",
  "url": "string",
  "summary": "string",
  "content": "string",
  "published_at": "datetime",
  "category": "string",
  "author": "string",
  "image_url": "string",
  "is_saved": false
}
```

## Error Handling
- Retry failed requests
- Handle rate limiting
- Log scraping errors
- Fallback to cached data