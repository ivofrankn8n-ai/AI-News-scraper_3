#!/usr/bin/env python3
"""
Migration script to move existing articles from JSON files to Supabase
Run this once Supabase credentials are available
"""

import os
import json
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from simple_supabase_client import SimpleSupabaseClient
except ImportError:
    print("ERROR: SimpleSupabaseClient not available")
    sys.exit(1)

def migrate_articles():
    """Migrate articles from JSON files to Supabase"""
    
    # Check if Supabase credentials are available
    if not os.getenv('SUPABASE_ANON_KEY'):
        print("ERROR: SUPABASE_ANON_KEY environment variable not set")
        print("Please set SUPABASE_ANON_KEY before running migration")
        return False
    
    # Check if JSON files exist
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    processed_file = os.path.join(project_root, '.tmp', 'processed_articles.json')
    
    if not os.path.exists(processed_file):
        print("ERROR: Processed articles file not found")
        print(f"Expected: {processed_file}")
        return False
    
    try:
        # Initialize Supabase client
        client = SimpleSupabaseClient()
        
        # Load existing articles
        with open(processed_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        print(f"Found {len(articles)} articles to migrate")
        
        # Migrate articles
        migrated_count = client.migrate_existing_articles(processed_file)
        
        if migrated_count > 0:
            print(f"SUCCESS: Migrated {migrated_count} articles to Supabase")
            return True
        else:
            print("ERROR: No articles were migrated")
            return False
            
    except Exception as e:
        print(f"ERROR: Migration failed: {e}")
        return False

def main():
    """Main function"""
    print("AI News Dashboard - Supabase Migration Tool")
    print("=" * 50)
    
    if migrate_articles():
        print("\nMigration completed successfully!")
        print("The dashboard will now load articles from Supabase")
    else:
        print("\nMigration failed. Please check your Supabase credentials")
        print("and ensure the articles JSON file exists.")

if __name__ == "__main__":
    main()