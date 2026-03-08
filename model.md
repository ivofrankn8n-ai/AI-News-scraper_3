# AI_NEWS-3 Project Constitution

## Data Schema

### Input Data Shape
```json
{
  "article": {
    "id": "string",
    "title": "string", 
    "source": "string",
    "url": "string",
    "summary": "string",
    "published_at": "datetime",
    "content": "string",
    "category": "string",
    "author": "string",
    "image_url": "string"
  }
}
```

### Output Data Shape (Dashboard)
```json
{
  "dashboard": {
    "articles": ["article"],
    "last_updated": "datetime",
    "stats": {
      "total_articles": "number",
      "new_today": "number",
      "saved_count": "number"
    }
  }
}
```

## Behavioral Rules

- **Tone**: Professional, informative, engaging
- **Refresh Interval**: 24 hours
- **Data Persistence**: Saved articles persist across refreshes
- **UI Requirements**: Gorgeous, interactive, beautiful design
- **Sources**: Ben's Bytes, The AI Rundown, Reddit (starting with newsletters)

## Source of Truth
- Primary: Newsletter RSS/API feeds
- Secondary: Supabase database (future integration)

## Delivery Payload
- Interactive dashboard displaying latest articles
- 24-hour refresh cycle
- Persistent saved articles

## Constraints
- Start with newsletter scraping only
- Dashboard integration comes later
- Focus on beautiful, interactive UI