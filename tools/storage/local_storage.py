#!/usr/bin/env python3
"""
Local Storage Manager for AI News Dashboard
Manages saved articles and data persistence
"""

import json
import os
from datetime import datetime
import sys

# Add parent directory to path for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LocalStorage:
    def __init__(self):
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_dir = os.path.join(project_root, '.tmp')
        self.saved_file = os.path.join(self.data_dir, 'saved_articles.json')
        self.stats_file = os.path.join(self.data_dir, 'dashboard_stats.json')
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
    
    def load_saved_articles(self):
        """Load saved article IDs"""
        try:
            with open(self.saved_file, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        except FileNotFoundError:
            # Return empty set if file doesn't exist
            return set()
        except json.JSONDecodeError:
            print("Error reading saved articles file, starting fresh")
            return set()
    
    def save_article(self, article_id):
        """Save an article ID to the saved list"""
        saved_ids = self.load_saved_articles()
        saved_ids.add(article_id)
        
        with open(self.saved_file, 'w', encoding='utf-8') as f:
            json.dump(list(saved_ids), f, indent=2)
        
        print(f"Saved article: {article_id}")
        return True
    
    def unsave_article(self, article_id):
        """Remove an article ID from the saved list"""
        saved_ids = self.load_saved_articles()
        
        if article_id in saved_ids:
            saved_ids.remove(article_id)
            
            with open(self.saved_file, 'w', encoding='utf-8') as f:
                json.dump(list(saved_ids), f, indent=2)
            
            print(f"Unsaved article: {article_id}")
            return True
        
        return False
    
    def is_article_saved(self, article_id):
        """Check if an article is saved"""
        saved_ids = self.load_saved_articles()
        return article_id in saved_ids
    
    def update_saved_status(self, articles):
        """Update saved status for a list of articles"""
        saved_ids = self.load_saved_articles()
        
        for article in articles:
            article['is_saved'] = article['id'] in saved_ids
        
        return articles
    
    def load_dashboard_stats(self):
        """Load dashboard statistics"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default stats
            return {
                'total_articles': 0,
                'new_today': 0,
                'saved_count': 0,
                'last_updated': datetime.now().isoformat()
            }
        except json.JSONDecodeError:
            print("Error reading stats file, using defaults")
            return {
                'total_articles': 0,
                'new_today': 0,
                'saved_count': 0,
                'last_updated': datetime.now().isoformat()
            }
    
    def save_dashboard_stats(self, articles):
        """Calculate and save dashboard statistics"""
        saved_ids = self.load_saved_articles()
        
        # Calculate today's date for filtering
        today = datetime.now().date()
        today_articles = [
            article for article in articles 
            if self._is_today(article.get('published_at', ''))
        ]
        
        stats = {
            'total_articles': len(articles),
            'new_today': len(today_articles),
            'saved_count': len(saved_ids),
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        return stats
    
    def _is_today(self, date_string):
        """Check if date is today"""
        try:
            article_date = datetime.fromisoformat(date_string.replace('Z', '+00:00')).date()
            return article_date == datetime.now().date()
        except:
            return False
    
    def cleanup_old_data(self, days=7):
        """Clean up data older than specified days"""
        # This would be implemented for long-term data management
        # For now, we'll keep all data
        print("Data cleanup functionality would be implemented here")
        return True

def test_storage():
    """Test the storage functionality"""
    storage = LocalStorage()
    
    # Test saved articles
    test_id = "test_article_123"
    
    # Save article
    storage.save_article(test_id)
    
    # Check if saved
    is_saved = storage.is_article_saved(test_id)
    print(f"Article saved: {is_saved}")
    
    # Unsave article
    storage.unsave_article(test_id)
    
    # Check again
    is_saved = storage.is_article_saved(test_id)
    print(f"Article saved after unsave: {is_saved}")

if __name__ == "__main__":
    test_storage()