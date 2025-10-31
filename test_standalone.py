#!/usr/bin/env python3
"""
Standalone test script for news crawler functionality.
Tests the crawler without database dependencies - just the scraping logic.
This version can run outside Docker if you have the dependencies installed.
"""

import sys
import json
from typing import Dict, Any
from datetime import datetime
from dags.utils.scraper import Scraper


def test_portal(portal_name: str, portal_url: str, max_articles: int = 5) -> Dict[str, Any]:
    """Test scraping a single portal and extract article data."""
    print(f"\nTesting: {portal_name} - {portal_url}")
    
    result = {
        'portal_name': portal_name,
        'portal_url': portal_url,
        'success': False,
        'articles_found': 0,
        'articles_extracted': 0,
        'articles': [],
        'error': None
    }
    
    try:
        scraper = Scraper(portal_name, portal_url)
        response = scraper.fetch_page(portal_url)
        
        if not response:
            result['error'] = "Failed to fetch homepage"
            return result
        
        article_links = scraper.extract_article_links(response.text)
        result['articles_found'] = len(article_links)
        
        if article_links:
            # Limit to max_articles
            article_links = article_links[:max_articles]
            print(f"Found {len(article_links)} articles (extracting up to {max_articles})")
            
            # Extract data from each article
            for i, article_url in enumerate(article_links, 1):
                print(f"  Extracting article {i}/{len(article_links)}: {article_url}")
                article_response = scraper.fetch_page(article_url)
                
                if article_response:
                    article_data = scraper.extract_article_data(article_response.text, article_url)
                    if article_data:
                        result['articles'].append(article_data)
                        print(f"    ✓ Title: {article_data['title'][:50]}...")
                    else:
                        print(f"    ⚠ No valid title or content found")
                else:
                    print(f"    ⚠ Failed to fetch article")
            
            result['articles_extracted'] = len(result['articles'])
            if result['articles']:
                result['success'] = True
        else:
            result['error'] = "No article links found"
        
    except Exception as e:
        result['error'] = str(e)
    
    return result


def main():
    """Main test function."""
    PORTALS = [
        {"name": "IstoÉDinheiro", "url": "https://www.istoedinheiro.com.br/"},
        {"name": "MoneyTimes", "url": "https://moneytimes.com.br/"}
    ]
    
    print("\nNEWS CRAWLER TEST")
    results = []
    
    # Test specific portal if provided
    if len(sys.argv) > 1:
        portal_name = sys.argv[1]
        portal = next((p for p in PORTALS if p['name'].lower() == portal_name.lower()), None)
        
        if portal:
            result = test_portal(portal['name'], portal['url'])
            results.append(result)
        else:
            print(f"Portal '{portal_name}' not found")
            print(f"Available: {', '.join(p['name'] for p in PORTALS)}")
            return False
    else:
        for portal in PORTALS:
            result = test_portal(portal['name'], portal['url'])
            results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for result in results:
        status = "✓ PASSED" if result['success'] else "✗ FAILED"
        print(f"{result['portal_name']}: {status} - {result['articles_extracted']}/{result['articles_found']} articles extracted")
        if result['error']:
            print(f"  Error: {result['error']}")
    
    passed = sum(1 for r in results if r['success'])
    print(f"\n{passed}/{len(results)} portals working")
    
    # Save articles to JSON file
    output_data = {
        'timestamp': datetime.now().isoformat(),
        'portals': []
    }
    
    total_articles = 0
    for result in results:
        portal_data = {
            'portal_name': result['portal_name'],
            'portal_url': result['portal_url'],
            'articles_extracted': result['articles_extracted'],
            'articles_found': result['articles_found'],
            'success': result['success'],
            'articles': result['articles']
        }
        if result['error']:
            portal_data['error'] = result['error']
        output_data['portals'].append(portal_data)
        total_articles += result['articles_extracted']
    
    output_filename = 'articles_data.json'
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\n✓ Saved {total_articles} articles to {output_filename}\n")
    except Exception as e:
        print(f"\n✗ Failed to save JSON file: {e}\n")
    
    return all(r['success'] for r in results)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nInterrupted")
        sys.exit(1)
    except Exception as e:
        sys.exit(1)

