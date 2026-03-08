# AI News Dashboard 🤖

A beautiful, interactive dashboard that aggregates and displays the latest AI articles from top newsletters including Ben's Bytes and The AI Rundown.

## Features

✨ **Beautiful Design**: Modern glassmorphism design with gradient background  
📰 **Multi-Source Aggregation**: Scrapes articles from Ben's Bytes and The AI Rundown  
💾 **Persistent Storage**: Saved articles persist across browser sessions  
🔍 **Search & Filter**: Filter by source or search through article content  
📱 **Responsive Design**: Works perfectly on desktop and mobile  
🔄 **Auto-Refresh**: 24-hour refresh cycle (manual refresh available)  
🎯 **Stable Layout**: No layout shifts or visual jumps during interactions  

## Quick Start

1. **Run the pipeline** to fetch latest articles:
   ```bash
   python tools/run_pipeline.py
   ```

2. **Start the dashboard server**:
   ```bash
   python serve.py
   ```

3. **Open your browser** to `http://localhost:8000/dashboard.html`

Or use the batch file:
```bash
run.bat
```

## Project Structure

```
AI_NEWS-3/
├── dashboard.html          # Main dashboard interface
├── serve.py               # Local development server
├── run.bat                # Windows batch runner
├── model.md               # Project constitution & data schema
├── task_plan.md           # B.L.A.S.T. phases & progress
├── findings.md            # Research & technical learnings
├── progress.md            # Implementation progress
├── .env                   # Environment variables template
├── architecture/          # Technical SOPs & architecture
├── tools/                 # Python scripts & utilities
│   ├── scrapers/         # Newsletter scraping logic
│   ├── processors/       # Data normalization
│   └── storage/          # Local storage management
└── .tmp/                 # Temporary data storage
```

## B.L.A.S.T. Master System Implementation

This project follows the B.L.A.S.T. Master System Protocol:

### Phase 1: B - Blueprint ✅
- Defined project scope and data schemas
- Identified newsletter sources and integrations

### Phase 2: L - Link ✅
- Verified connectivity to newsletter APIs/RSS feeds
- Built reliable scraping infrastructure

### Phase 3: A - Architect ✅
- Created 3-layer architecture (SOPs → Navigation → Tools)
- Implemented deterministic Python scripts

### Phase 4: S - Stylize ✅
- Designed beautiful, interactive dashboard
- Implemented professional UI/UX

### Phase 5: T - Trigger ✅ COMPLETED
- Dashboard fully polished and stable
- Layout shift issues resolved
- Production-ready design

## Data Flow

1. **Scraping**: Python scripts fetch articles from RSS feeds and websites
2. **Processing**: Data is normalized and filtered (last 24 hours)
3. **Storage**: Articles saved to JSON files, saved articles to localStorage
4. **Display**: Dashboard renders articles with interactive features

## Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python 3.x with requests, BeautifulSoup
- **Storage**: JSON files + localStorage
- **Styling**: Modern CSS with gradients and animations

## Customization

### Adding New Sources
1. Add scraper in `tools/scrapers/`
2. Update data schema in `model.md`
3. Add source filter in `dashboard.html`

### Styling Changes
- Modify CSS variables in `dashboard.html`
- Update card layouts and animations

## Development

### Running Tests
```bash
python tools/scrapers/newsletter_scraper.py  # Test scraper
python tools/processors/data_processor.py    # Test processor
python tools/storage/local_storage.py       # Test storage
```

### Data Files
- `.tmp/articles.json`: Raw scraped articles
- `.tmp/processed_articles.json`: Normalized articles
- Browser localStorage: Saved article IDs

## Next Steps

- [x] Implement automated 24-hour refresh ✅
- [x] Fix layout shift issues ✅
- [x] Consolidate dashboard files ✅
- [x] Polish scrollbar and search interactions ✅
- [ ] Add Reddit integration
- [ ] Deploy to cloud platform
- [ ] Add email notifications
- [ ] Implement user accounts

---

Built with ❤️ using the B.L.A.S.T. Master System Protocol