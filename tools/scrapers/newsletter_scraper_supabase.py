#!/usr/bin/env python3
"""
Supabase-enabled Newsletter Scraper for AI News Dashboard
Based on the working newsletter_scraper.py
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import hashlib
import json
import os
from urllib.parse import urlparse
import time
import sys
from dotenv import load_dotenv

# Add parent directory to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from simple_supabase_client import SimpleSupabaseClient
except ImportError:
    SimpleSupabaseClient = None

class NewsletterScraperSupabase:
    def __init__(self, use_supabase=True):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AI_NEWS-3 Scraper/1.0)',
            'Accept': 'application/rss+xml,text/html,application/xhtml+xml'
        })
        
        self.use_supabase = use_supabase
        self.supabase_client = None
        
        if use_supabase and SimpleSupabaseClient:
            try:
                self.supabase_client = SimpleSupabaseClient()
                print("SUCCESS: Supabase client initialized")
            except Exception as e:
                print(f"ERROR: Failed to initialize Supabase client: {e}")
                self.use_supabase = False
        
    def scrape_bens_bites(self):
        """Scrape Ben's Bytes RSS feed"""
        print("Scraping Ben's Bytes...")
        
        try:
            response = self.session.get('https://bensbites.substack.com/feed')
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            articles = []
            
            # Parse RSS items
            for item in root.findall('.//item')[:10]:  # Limit to 10 latest
                article = self._parse_rss_item(item, 'bens_bites')
                if article:
                    articles.append(article)
            
            print(f"Found {len(articles)} articles from Ben's Bytes")
            return articles
            
        except Exception as e:
            print(f"Error scraping Ben's Bytes: {e}")
            return []
    
    def scrape_ai_rundown(self):
        """Scrape The AI Rundown articles"""
        print("Scraping The AI Rundown...")
        
        try:
            # Get latest articles from sitemap
            response = self.session.get('https://www.therundown.ai/sitemap.xml')
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            articles = []
            
            # Extract article URLs from sitemap
            article_urls = []
            for url in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None and '/p/' in loc.text:
                    article_urls.append(loc.text)
            
            # Get latest 10 articles
            for url in article_urls[:10]:
                article = self._scrape_ai_rundown_article(url)
                if article:
                    articles.append(article)
                time.sleep(1)  # Be respectful
            
            print(f"Found {len(articles)} articles from The AI Rundown")
            return articles
            
        except Exception as e:
            print(f"Error scraping The AI Rundown: {e}")
            return []
    
    def _scrape_ai_rundown_article(self, url):
        """Scrape individual AI Rundown article"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            # Basic article info from URL
            article_id = self._generate_id(url)
            
            return {
                'id': article_id,
                'title': 'AI Rundown Article',  # Would need proper parsing
                'source': 'ai_rundown',
                'url': url,
                'summary': 'Latest AI news from The AI Rundown',
                'published_at': datetime.now().isoformat(),
                'category': 'AI News',
                'author': 'The AI Rundown Team',
                'image_url': ''
            }
            
        except Exception as e:
            print(f"Error scraping AI Rundown article {url}: {e}")
            return None
    
    def _parse_rss_item(self, item, source):
        """Parse RSS item into article dictionary"""
        try:
            title = item.find('title')
            link = item.find('link')
            pub_date = item.find('pubDate')
            description = item.find('description')
            
            # Check if elements exist and have text
            if title is None or link is None:
                return None
            
            title_text = title.text if title.text else ''
            link_text = link.text if link.text else ''
            
            if not title_text or not link_text:
                return None
            
            # Generate ID from URL
            article_id = self._generate_id(link_text)
            
            # Parse publication date
            published_at = self._parse_rss_date(pub_date.text if pub_date else None)
            
            # Clean description
            summary_text = description.text if description else ''
            summary = self._clean_html(summary_text)
            
            article = {
                'id': article_id,
                'title': title_text.strip(),
                'source': source,
                'url': link_text,
                'summary': summary[:200] + '...' if len(summary) > 200 else summary,
                'published_at': published_at,
                'category': 'AI News',
                'author': 'Ben Tossell' if source == 'bens_bites' else 'Unknown',
                'image_url': ''
            }
            
            return article
            
        except Exception as e:
            print(f"Error parsing RSS item: {e}")
            return None
    
    def _parse_rss_date(self, date_str):
        """Parse RSS date string"""
        if not date_str:
            return datetime.now().isoformat()
        
        try:
            # Try various date formats
            formats = [
                '%a, %d %b %Y %H:%M:%S %Z',
                '%a, %d %b %Y %H:%M:%S %z',
                '%Y-%m-%dT%H:%M:%S%z'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.isoformat()
                except ValueError:
                    continue
            
            # Fallback to current time
            return datetime.now().isoformat()
            
        except Exception:
            return datetime.now().isoformat()
    
    def _clean_html(self, text):
        """Basic HTML cleaning"""
        if not text:
            return ''
        
        # Remove HTML tags (basic)
        import re
        clean = re.sub(r'<[^>]+>', '', text)
        return clean.strip()
    
    def _generate_id(self, url):
        """Generate unique ID from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def filter_recent_articles(self, articles, hours=24):
        """Filter articles from last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_articles = []
        
        for article in articles:
            try:
                # Parse publication date
                pub_date = datetime.fromisoformat(article['published_at'].replace('Z', '+00:00'))
                if pub_date >= cutoff_time:
                    recent_articles.append(article)
            except:
                # If date parsing fails, include article
                recent_articles.append(article)
        
        return recent_articles
    
    def save_articles(self, articles, filepath=None):
        """Save articles to Supabase or local file"""
        if self.use_supabase and self.supabase_client:
            # Save to Supabase
            saved_count = 0
            for article in articles:
                result = self.supabase_client.upsert_article(article)
                if result:
                    saved_count += 1
            
            print(f"SUCCESS: Saved {saved_count}/{len(articles)} articles to Supabase")
            return saved_count > 0
        else:
            # Fallback to local file
            if not filepath:
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                filepath = os.path.join(project_root, '.tmp', 'articles.json')
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=2, ensure_ascii=False)
            
            print(f"SUCCESS: Saved {len(articles)} articles to {filepath}")
            return True
    
    def scrape_all(self):
        """Scrape articles from all sources"""
        print("Starting newsletter scraping...")
        
        # Scrape Ben's Bytes
        bens_articles = self.scrape_bens_bites()
        
        # Scrape AI Rundown
        ai_rundown_articles = self.scrape_ai_rundown()
        
        # Combine articles
        all_articles = bens_articles + ai_rundown_articles
        
        # Filter recent articles (last 6 hours to avoid duplicates)
        recent_articles = self.filter_recent_articles(all_articles, hours=6)
        
        print(f"Total recent articles: {len(recent_articles)}")
        
        # Save articles
        if recent_articles:
            self.save_articles(recent_articles)
        
        return recent_articles

def main():
    """Main function"""
    # Load environment variables from .env file
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(project_root, '.env')
    load_dotenv(env_path)
    
    # Check if Supabase is available
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    supabase_url = os.getenv('SUPABASE_URL')
    use_supabase = supabase_key is not None
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key available: {supabase_key is not None}")
    print(f"Using Supabase: {use_supabase}")
    
    if use_supabase:
        print("Attempting to initialize Supabase client...")
    
    scraper = NewsletterScraperSupabase(use_supabase=use_supabase)
    articles = scraper.scrape_all()
    
    if articles:
        print(f"SUCCESS: Successfully scraped {len(articles)} articles")
        return articles
    else:
        print("ERROR: No articles scraped")
        return []

if __name__ == "__main__":
    main()