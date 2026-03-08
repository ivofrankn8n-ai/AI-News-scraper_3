#!/usr/bin/env python3
"""
Modal.com Scheduled Scraper for AI News Dashboard
Runs every 3 hours to scrape articles from Ben's Bytes and AI Rundown
"""

import modal
import os
from datetime import datetime

# Create Modal app
app = modal.App("ai-news-scraper")

# Image with required dependencies
image = (
    modal.Image.debian_slim()
    .pip_install("requests", "beautifulsoup4", "python-dotenv", "httpx")
)

@app.function(image=image, schedule=modal.Cron("0 */3 * * *"))  # Every 3 hours
def scrape_articles():
    """
    Scheduled function that runs every 3 hours.
    Scrapes articles from Ben's Bytes and AI Rundown, then updates Supabase.
    """
    import requests
    import xml.etree.ElementTree as ET
    from datetime import datetime, timedelta
    import hashlib
    
    # Get Supabase credentials from Modal secrets
    supabase_url = os.environ.get("SUPABASE_URL", "https://keajnbcsqgyfgyikvbca.supabase.co")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")  # Use service key for writing
    
    if not supabase_key:
        print("ERROR: SUPABASE_SERVICE_KEY not found in environment")
        return {"success": False, "error": "Missing SUPABASE_SERVICE_KEY"}
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (compatible; AI_NEWS-3 Scraper/1.0)',
        'Accept': 'application/rss+xml,text/html,application/xhtml+xml'
    })
    
    articles_scraped = 0
    
    # --- Scrape Ben's Bytes ---
    try:
        print("Scraping Ben's Bytes...")
        response = session.get('https://bensbites.substack.com/feed')
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item'):
            try:
                title = item.find('title').text
                link = item.find('link').text
                pub_date = item.find('pubDate').text
                description = item.find('description').text or ""
                
                # Parse date
                published_at = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                published_at = published_at.isoformat()
                
                # Check if already today
                if 'T' in published_at:
                    date_part = published_at.split('T')[0]
                    if date_part != datetime.now().strftime('%Y-%m-%d'):
                        continue  # Skip articles not from today
                
                # Generate unique ID
                article_id = hashlib.md5(f"{title}{link}".encode()).hexdigest()
                
                # Upsert article
                article_data = {
                    "id": article_id,
                    "title": title,
                    "url": link,
                    "summary": description[:500] if description else "",
                    "source": "bens_bites",
                    "author": "Ben Tossell",
                    "published_at": published_at,
                    "category": "AI News"
                }
                
                url = f"{supabase_url}/rest/v1/articles"
                resp = requests.post(url, json=article_data, headers=headers)
                
                if resp.status_code in [200, 201]:
                    articles_scraped += 1
                    print(f"  ✓ Added: {title[:50]}...")
                elif resp.status_code == 409:
                    print(f"  - Already exists: {title[:50]}")
                else:
                    print(f"  ✗ Error: {resp.status_code} - {resp.text[:100]}")
                    
            except Exception as e:
                print(f"  ✗ Error processing item: {e}")
                continue
                
        print(f"Ben's Bytes: {articles_scraped} articles processed")
        
    except Exception as e:
        print(f"Error scraping Ben's Bytes: {e}")
    
    # --- Scrape AI Rundown ---
    try:
        print("Scraping AI Rundown...")
        response = session.get('https://www.therundown.ai/sitemap.xml')
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        ai_rundown_count = 0
        
        # Get last 20 URLs from sitemap
        urls = []
        for url in root.findall('.//url')[:20]:
            loc = url.find('loc')
            if loc is not None:
                urls.append(loc.text)
        
        for article_url in urls:
            try:
                # Fetch article page
                article_resp = session.get(article_url)
                if article_resp.status_code != 200:
                    continue
                
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(article_resp.text, 'html.parser')
                
                # Extract title
                title_tag = soup.find('title')
                title = title_tag.text if title_tag else "AI Rundown Article"
                
                # Extract description from meta tags
                desc_tag = soup.find('meta', attrs={'name': 'description'})
                description = desc_tag.get('content', '') if desc_tag else ""
                
                # Generate ID
                article_id = hashlib.md5(f"{title}{article_url}".encode()).hexdigest()
                
                # Use current time for published_at
                published_at = datetime.now().isoformat()
                
                article_data = {
                    "id": article_id,
                    "title": title,
                    "url": article_url,
                    "summary": description[:500] if description else "",
                    "source": "ai_rundown",
                    "author": "The Rundown AI",
                    "published_at": published_at,
                    "category": "AI News"
                }
                
                url = f"{supabase_url}/rest/v1/articles"
                resp = requests.post(url, json=article_data, headers=headers)
                
                if resp.status_code in [200, 201]:
                    ai_rundown_count += 1
                    print(f"  ✓ Added: {title[:50]}...")
                elif resp.status_code == 409:
                    print(f"  - Already exists: {title[:50]}")
                else:
                    print(f"  ✗ Error: {resp.status_code}")
                    
            except Exception as e:
                print(f"  ✗ Error processing article: {e}")
                continue
        
        print(f"AI Rundown: {ai_rundown_count} articles processed")
        articles_scraped += ai_rundown_count
        
    except Exception as e:
        print(f"Error scraping AI Rundown: {e}")
    
    # --- Update scraper metadata ---
    try:
        print("Updating scraper metadata...")
        metadata_url = f"{supabase_url}/rest/v1/scraper_metadata?source=eq.all"
        
        # First try to update
        update_data = {"last_scraped_at": datetime.now().isoformat()}
        resp = requests.patch(metadata_url, json=update_data, headers=headers)
        
        if resp.status_code == 200:
            print("✓ Metadata updated")
        else:
            # If no row exists, insert one
            insert_headers = headers.copy()
            insert_headers["Prefer"] = "return=representation"
            insert_resp = requests.post(
                f"{supabase_url}/rest/v1/scraper_metadata",
                json={"source": "all", "last_scraped_at": datetime.now().isoformat()},
                headers=insert_headers
            )
            if insert_resp.status_code in [200, 201]:
                print("✓ Metadata created")
            else:
                print(f"  ✗ Metadata error: {insert_resp.status_code}")
                
    except Exception as e:
        print(f"Error updating metadata: {e}")
    
    print(f"\n=== Scraping complete! Total: {articles_scraped} articles ===")
    return {"success": True, "articles_scraped": articles_scraped}


# For local testing - run once without Modal scheduling
if __name__ == "__main__":
    print("Running scraper locally (not on Modal)...")
    scrape_articles()
