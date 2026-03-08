# Dashboard Architecture

## Goal
Beautiful, interactive dashboard displaying latest AI articles with saved article functionality

## UI Components

### Layout Structure
```
┌─────────────────────────────────────────┐
│ Header: AI News Dashboard               │
├─────────────────────────────────────────┤
│ Stats Bar: Total Articles | New Today   │
├─────────────────────────────────────────┤
│ Article Grid:                           │
│ ┌───────┐ ┌───────┐ ┌───────┐           │
│ │Article│ │Article│ │Article│           │
│ │ Card  │ │ Card  │ │ Card  │           │
│ └───────┘ └───────┘ └───────┘           │
│                                         │
│ [Load More] [Filter by Source]          │
└─────────────────────────────────────────┘
```

### Article Card Design
- Clean, modern card layout
- Source badge (Ben's Bytes / AI Rundown)
- Save/Unsave button (heart icon)
- Publication date
- Excerpt/preview
- Read more link

### Interactive Features
- Save/unsave articles (persistent across refreshes)
- Filter by source
- Search functionality
- Responsive design

## Technical Stack
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Modern CSS with gradients, shadows
- **Storage**: LocalStorage for saved articles
- **Data**: JSON files from scraper

## Data Flow
1. Load articles from `.tmp/articles.json`
2. Load saved article IDs from localStorage
3. Render article cards with save state
4. Handle user interactions
5. Update localStorage on save/unsave