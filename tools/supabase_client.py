#!/usr/bin/env python3
"""
Supabase Client Utility for AI News Dashboard
Handles database operations for articles
"""

import os
import hashlib
from datetime import datetime
from supabase import create_client, Client

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client with environment variables"""
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY', '')
        
        if not self.key:
            raise ValueError("SUPABASE_ANON_KEY environment variable is required")
        
        self.client: Client = create_client(self.url, self.key)
    
    def generate_article_id(self, url: str) -> str:
        """Generate consistent article ID from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def upsert_article(self, article_data: dict) -> dict:
        """Insert or update article in Supabase"""
        # Ensure required fields
        if not article_data.get('url') or not article_data.get('title'):
            raise ValueError("Article must have URL and title")
        
        # Generate ID from URL
        article_id = self.generate_article_id(article_data['url'])
        
        # Prepare data for Supabase
        supabase_article = {
            'id': article_id,
            'title': article_data.get('title', ''),
            'subtitle': article_data.get('summary', ''),
            'url': article_data['url'],
            'source': article_data.get('source', 'unknown'),
            'published_at': article_data.get('published_at'),
            'summary': article_data.get('summary', ''),
            'author': article_data.get('author', 'Unknown'),
            'category': article_data.get('category', 'AI News'),
            'image_url': article_data.get('image_url', ''),
            'created_at': datetime.now().isoformat()
        }
        
        # Remove None values
        supabase_article = {k: v for k, v in supabase_article.items() if v is not None}
        
        try:
            # Upsert article (insert or update on conflict)
            response = self.client.table('articles').upsert(supabase_article).execute()
            
            if response.data:
                print(f"✓ Upserted article: {article_data['title'][:50]}...")
                return response.data[0]
            else:
                print(f"✗ Failed to upsert article: {article_data['title'][:50]}...")
                return None
                
        except Exception as e:
            print(f"✗ Error upserting article {article_data['title'][:50]}: {e}")
            return None
    
    def get_all_articles(self) -> list:
        """Get all articles from Supabase"""
        try:
            response = self.client.table('articles').select('*').order('published_at', desc=True).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"✗ Error fetching articles from Supabase: {e}")
            return []
    
    def migrate_existing_articles(self, json_file_path: str) -> int:
        """Migrate existing articles from JSON file to Supabase"""
        import json
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            migrated_count = 0
            for article in articles:
                result = self.upsert_article(article)
                if result:
                    migrated_count += 1
            
            print(f"✓ Migrated {migrated_count}/{len(articles)} articles to Supabase")
            return migrated_count
            
        except Exception as e:
            print(f"✗ Error migrating articles: {e}")
            return 0

def test_connection():
    """Test Supabase connection"""
    try:
        client = SupabaseClient()
        articles = client.get_all_articles()
        print(f"✓ Supabase connection successful. Found {len(articles)} articles")
        return True
    except Exception as e:
        print(f"✗ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test the connection
    if test_connection():
        print("Supabase client is working correctly!")
    else:
        print("Please set SUPABASE_ANON_KEY environment variable")