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

@app.function(
    image=image, 
    schedule=modal.Cron("0 */3 * * *"),  # Every 3 hours
    secrets=[modal.Secret.from_name("supabase-secret")]
)
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
    ben_bytes_count = 0
    try:
        print("Scraping Ben's Bytes...")
        response = session.get('https://www.bensbites.com/feed')
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item'):
            try:
                title = item.find('title').text
                link = item.find('link').text
                pub_date = item.find('pubDate').text
                description = item.find('description').text or ""
                
                # Parse date - handle both with and without timezone
                try:
                    published_at = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                except ValueError:
                    # Try parsing without timezone
                    published_at = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S GMT')
                    # Add UTC timezone
                    published_at = published_at.replace(tzinfo=datetime.now().astimezone().tzinfo)
                
                # Check if from today (UTC calendar date)
                from datetime import timezone
                utc_now = datetime.now(timezone.utc)
                if published_at.astimezone(timezone.utc).date() != utc_now.date():
                    continue  # Skip articles not from today
                
                published_at = published_at.isoformat()
                
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
                    ben_bytes_count += 1
                    print(f"  [+] Added: {title[:50]}...")
                elif resp.status_code == 409:
                    print(f"  [-] Already exists: {title[:50]}")
                else:
                    print(f"  [-] Error: {resp.status_code} - {resp.text[:100]}")
                    
            except Exception as e:
                print(f"  [-] Error processing item: {e}")
                continue
                
        print(f"Ben's Bytes: {ben_bytes_count} articles processed")
        articles_scraped += ben_bytes_count
        
    except Exception as e:
        print(f"Error scraping Ben's Bytes: {e}")
    
    # --- Scrape AI Rundown ---
    ai_rundown_count = 0
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            print(f"Scraping AI Rundown (attempt {attempt + 1}/{max_retries})...")
            response = session.get('https://therundown.substack.com/feed', timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            for item in root.findall('.//item'):
                try:
                    title = item.find('title').text
                    link = item.find('link').text
                    pub_date = item.find('pubDate').text
                    description = item.find('description').text or ""
                    
                    # Parse date - handle both with and without timezone
                    try:
                        published_at = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %z')
                    except ValueError:
                        # Try parsing without timezone
                        published_at = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S GMT')
                        # Add UTC timezone
                        published_at = published_at.replace(tzinfo=datetime.now().astimezone().tzinfo)
                    
                    # Check if from today (UTC calendar date)
                    from datetime import timezone
                    utc_now = datetime.now(timezone.utc)
                    if published_at.astimezone(timezone.utc).date() != utc_now.date():
                        continue  # Skip articles not from today
                    
                    published_at = published_at.isoformat()
                    
                    # Generate unique ID
                    article_id = hashlib.md5(f"{title}{link}".encode()).hexdigest()
                    
                    # Upsert article
                    article_data = {
                        "id": article_id,
                        "title": title,
                        "url": link,
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
                        print(f"  [+] Added: {title[:50]}...")
                    elif resp.status_code == 409:
                        print(f"  [-] Already exists: {title[:50]}")
                    else:
                        print(f"  [-] Error: {resp.status_code}")
                        
                except Exception as e:
                    print(f"  [-] Error processing item: {e}")
                    continue
            
            print(f"AI Rundown: {ai_rundown_count} articles processed")
            articles_scraped += ai_rundown_count
            break  # Success, exit retry loop
            
        except Exception as e:
            print(f"Error scraping AI Rundown (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                print("Retrying in 5 seconds...")
                import time
                time.sleep(5)
            else:
                print("Max retries reached, skipping AI Rundown for this run")
    
    # --- Update scraper metadata ---
    try:
        print("Updating scraper metadata...")
        metadata_url = f"{supabase_url}/rest/v1/scraper_metadata?source=eq.all"
        
        # Try to update existing record
        update_data = {"last_scraped_at": datetime.now().isoformat()}
        resp = requests.patch(metadata_url, json=update_data, headers=headers)
        
        if resp.status_code == 200:
            print("[+] Metadata updated")
        else:
            print(f"  [-] Metadata update failed: {resp.status_code}")
                
    except Exception as e:
        print(f"Error updating metadata: {e}")
    
    print(f"\n=== Scraping complete! Total: {articles_scraped} articles ===")
    return {"success": True, "articles_scraped": articles_scraped}


# For local testing - run once without Modal scheduling
if __name__ == "__main__":
    print("Running scraper locally (not on Modal)...")
    scrape_articles()
