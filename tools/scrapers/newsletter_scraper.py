#!/usr/bin/env python3
"""
Newsletter Scraper for AI News Dashboard
Scrapes articles from Ben's Bytes and The AI Rundown
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

# Add parent directory to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class NewsletterScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AI_NEWS-3 Scraper/1.0)',
            'Accept': 'application/rss+xml,text/html,application/xhtml+xml'
        })
        
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
            
            # Simple HTML parsing for title and date
            # In a real implementation, you'd use BeautifulSoup
            content = response.text
            
            # Extract title from meta tags
            title_start = content.find('<title>') + 7
            title_end = content.find('</title>')
            title = content[title_start:title_end].strip() if title_start > 6 else 'Unknown Title'
            
            # Generate article data
            article = {
                'id': self._generate_id(url),
                'title': title,
                'source': 'ai_rundown',
                'url': url,
                'summary': 'AI news article from The AI Rundown',
                'content': '',  # Would extract actual content
                'published_at': datetime.now().isoformat(),
                'category': 'AI News',
                'author': 'The Rundown Team',
                'image_url': '',
                'is_saved': False
            }
            
            return article
            
        except Exception as e:
            print(f"Error scraping article {url}: {e}")
            return None
    
    def _parse_rss_item(self, item, source):
        """Parse RSS item into article format"""
        try:
            title = item.find('title').text if item.find('title') is not None else 'Unknown Title'
            link = item.find('link').text if item.find('link') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else datetime.now().isoformat()
            description = item.find('description').text if item.find('description') is not None else ''
            
            # Clean up description
            if description:
                description = description.replace('<p>', '').replace('</p>', '')
            
            article = {
                'id': self._generate_id(link),
                'title': title,
                'source': source,
                'url': link,
                'summary': description[:200] + '...' if len(description) > 200 else description,
                'content': description,
                'published_at': pub_date,
                'category': 'AI News',
                'author': 'Ben Tossell' if source == 'bens_bites' else 'Unknown',
                'image_url': '',
                'is_saved': False
            }
            
            return article
            
        except Exception as e:
            print(f"Error parsing RSS item: {e}")
            return None
    
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

def main():
    """Main scraping function"""
    scraper = NewsletterScraper()
    
    # Scrape both sources
    bens_bites_articles = scraper.scrape_bens_bites()
    ai_rundown_articles = scraper.scrape_ai_rundown()
    
    # Combine articles
    all_articles = bens_bites_articles + ai_rundown_articles
    
    # Filter recent articles
    recent_articles = scraper.filter_recent_articles(all_articles)
    
    # Save to file
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_file = os.path.join(project_root, '.tmp', 'articles.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(recent_articles, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(recent_articles)} recent articles to {output_file}")
    
    return recent_articles

if __name__ == "__main__":
    main()