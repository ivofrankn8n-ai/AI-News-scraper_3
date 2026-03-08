#!/usr/bin/env python3
"""
Data Processor for AI News Dashboard
Normalizes and processes scraped article data
"""

import json
import os
from datetime import datetime
import hashlib
import sys

# Add parent directory to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DataProcessor:
    def __init__(self):
        self.processed_data = []
    
    def load_articles(self, filepath):
        """Load articles from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Articles file not found: {filepath}")
            return []
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {filepath}")
            return []
    
    def normalize_articles(self, articles):
        """Normalize article data structure"""
        normalized = []
        
        for article in articles:
            normalized_article = {
                'id': article.get('id', self._generate_id(article.get('url', ''))),
                'title': article.get('title', 'Untitled').strip(),
                'source': article.get('source', 'unknown'),
                'url': article.get('url', ''),
                'summary': self._clean_summary(article.get('summary', '')),
                'content': article.get('content', ''),
                'published_at': self._normalize_date(article.get('published_at')),
                'category': article.get('category', 'AI News'),
                'author': article.get('author', 'Unknown'),
                'image_url': article.get('image_url', ''),
                'is_saved': article.get('is_saved', False)
            }
            
            # Ensure required fields
            if normalized_article['title'] and normalized_article['url']:
                normalized.append(normalized_article)
        
        return normalized
    
    def _clean_summary(self, summary):
        """Clean and truncate summary"""
        if not summary:
            return "No summary available"
        
        # Remove HTML tags and extra whitespace
        import re
        cleaned = re.sub(r'<[^>]+>', '', summary)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Truncate to reasonable length
        if len(cleaned) > 300:
            return cleaned[:297] + '...'
        
        return cleaned
    
    def _normalize_date(self, date_string):
        """Normalize date format"""
        if not date_string:
            return datetime.now().isoformat()
        
        try:
            # Handle various date formats
            if 'T' in date_string:
                # ISO format
                return date_string.replace('Z', '+00:00')
            else:
                # Try parsing other formats
                formats = [
                    '%a, %d %b %Y %H:%M:%S %Z',  # RSS format
                    '%Y-%m-%d %H:%M:%S',
                    '%Y-%m-%d'
                ]
                
                for fmt in formats:
                    try:
                        dt = datetime.strptime(date_string, fmt)
                        return dt.isoformat()
                    except ValueError:
                        continue
                
                # Fallback to current time
                return datetime.now().isoformat()
                
        except Exception:
            return datetime.now().isoformat()
    
    def _generate_id(self, url):
        """Generate unique ID from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def sort_by_date(self, articles):
        """Sort articles by publication date (newest first)"""
        return sorted(articles, key=lambda x: x['published_at'], reverse=True)
    
    def save_processed_data(self, articles, filepath):
        """Save processed articles to file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(articles)} processed articles to {filepath}")

def process_articles():
    """Main processing function"""
    processor = DataProcessor()
    
    # Load scraped articles
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    articles_file = os.path.join(project_root, '.tmp', 'articles.json')
    articles = processor.load_articles(articles_file)
    
    if not articles:
        print("No articles found to process")
        return []
    
    # Normalize and process
    normalized = processor.normalize_articles(articles)
    sorted_articles = processor.sort_by_date(normalized)
    
    # Save processed data
    output_file = os.path.join(project_root, '.tmp', 'processed_articles.json')
    processor.save_processed_data(sorted_articles, output_file)
    
    print(f"Processed {len(sorted_articles)} articles")
    return sorted_articles

if __name__ == "__main__":
    process_articles()