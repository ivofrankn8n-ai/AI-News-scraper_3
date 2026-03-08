#!/usr/bin/env python3
"""
Main Pipeline Runner for AI News Dashboard
Coordinates scraping, processing, and storage
"""

import sys
import os

# Add tools directory to path
sys.path.append(os.path.dirname(__file__))

from scrapers.newsletter_scraper_supabase import main as scrape_articles
from processors.data_processor import process_articles
from storage.local_storage import LocalStorage

def run_full_pipeline():
    """Run the complete AI news pipeline"""
    print("Starting AI News Pipeline...")
    
    # Step 1: Scrape articles
    print("\nStep 1: Scraping articles...")
    articles = scrape_articles()
    
    if not articles:
        print("No articles scraped, pipeline stopping")
        return False
    
    # Step 2: Process articles
    print("\nStep 2: Processing articles...")
    processed_articles = process_articles()
    
    if not processed_articles:
        print("No articles processed, pipeline stopping")
        return False
    
    # Step 3: Update storage and stats
    print("\nStep 3: Updating storage...")
    storage = LocalStorage()
    
    # Update saved status
    articles_with_saved = storage.update_saved_status(processed_articles)
    
    # Save stats
    stats = storage.save_dashboard_stats(articles_with_saved)
    
    print(f"\nPipeline completed successfully!")
    print(f"Statistics:")
    print(f"   • Total articles: {stats['total_articles']}")
    print(f"   • New today: {stats['new_today']}")
    print(f"   • Saved articles: {stats['saved_count']}")
    print(f"   • Last updated: {stats['last_updated']}")
    
    return True

def main():
    """Main function"""
    try:
        success = run_full_pipeline()
        if success:
            print("\nReady to build the dashboard!")
            print("Run the dashboard HTML file to view your AI news")
        else:
            print("\nPipeline failed")
            sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()