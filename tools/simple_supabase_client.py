#!/usr/bin/env python3
"""
Simple Supabase Client using requests
For compatibility with older supabase-py versions
"""

import requests
import json
import os
import hashlib
from datetime import datetime
from dotenv import load_dotenv

class SimpleSupabaseClient:
    def __init__(self):
        self.url = os.getenv('SUPABASE_URL')
        self.key = os.getenv('SUPABASE_ANON_KEY', '')
        
        if not self.key:
            raise ValueError("SUPABASE_ANON_KEY environment variable is required")
        
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
    
    def generate_article_id(self, url: str) -> str:
        """Generate consistent article ID from URL"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def upsert_article(self, article_data: dict) -> dict:
        """Insert or update article in Supabase using REST API"""
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
            # Upsert using Supabase REST API
            response = requests.post(
                f"{self.url}/rest/v1/articles",
                headers=self.headers,
                json=supabase_article,
                params={"on_conflict": "id"}
            )
            
            if response.status_code in [200, 201]:
                print(f"SUCCESS: Upserted article: {article_data['title'][:50].encode('utf-8', 'ignore').decode('utf-8')}...")
                return response.json()[0] if response.json() else supabase_article
            else:
                print(f"FAILED: Failed to upsert article: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"ERROR: Error upserting article {article_data['title'][:50].encode('utf-8', 'ignore').decode('utf-8')}: {e}")
            return None
    
    def get_all_articles(self) -> list:
        """Get all articles from Supabase using REST API"""
        try:
            response = requests.get(
                f"{self.url}/rest/v1/articles",
                headers=self.headers,
                params={
                    "select": "*",
                    "order": "published_at.desc"
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"ERROR: Error fetching articles: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"ERROR: Error fetching articles from Supabase: {e}")
            return []
    
    def migrate_existing_articles(self, json_file_path: str) -> int:
        """Migrate existing articles from JSON file to Supabase"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            migrated_count = 0
            for article in articles:
                result = self.upsert_article(article)
                if result:
                    migrated_count += 1
            
            print(f"SUCCESS: Migrated {migrated_count}/{len(articles)} articles to Supabase")
            return migrated_count
            
        except Exception as e:
            print(f"ERROR: Error migrating articles: {e}")
            return 0

def test_connection():
    """Test Supabase connection"""
    try:
        client = SimpleSupabaseClient()
        articles = client.get_all_articles()
        print(f"SUCCESS: Supabase connection successful. Found {len(articles)} articles")
        return True
    except Exception as e:
        print(f"ERROR: Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    # Load environment variables from .env file
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(project_root, '.env')
    load_dotenv(env_path)
    
    # Test the connection
    if test_connection():
        print("Simple Supabase client is working correctly!")
    else:
        print("Please set SUPABASE_ANON_KEY environment variable")