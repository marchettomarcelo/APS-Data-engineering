from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup



class Scraper:
    """Minimal scraper for testing purposes."""
    
    def __init__(self, portal_name: str, portal_url: str):
        self.portal_name = portal_name
        self.portal_url = portal_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_page(self, url: str, timeout: int = 30):
        """Fetch a web page."""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            
            return None
    
    def parse_html(self, html_content: str):
        """Parse HTML content."""
        return BeautifulSoup(html_content, 'lxml')
    
    def extract_article_links(self, html_content: str) -> List[str]:
        """Extract article links from HTML."""
        soup = self.parse_html(html_content)
        links = set()
        
        # Common selectors for news articles
        selectors = [
            'article a',
            'h2 a',
            'h3 a',
            '.post-title a',
            '.entry-title a',
            '.news-item a',
            'a[href*="/noticia"]',
            'a[href*="/news"]',
            'a[href*="/article"]'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href')
                if href and href.startswith('http'):
                    # Basic filtering
                    if not any(skip in href for skip in ['#', '.pdf', '.jpg', '.png', '/tag/', '/author/']):
                        links.add(href)
        
        return list(links)
    
    def extract_article_data(self, html_content: str, article_url: str) -> Optional[Dict[str, Any]]:
        """
        Extract title and content from an article page.
        
        Returns None if no valid title or content is found, or if the content
        is too short to be meaningful (less than 100 characters).
        """
        soup = self.parse_html(html_content)
        
        # Try multiple selectors for title
        title = None
        title_selectors = [
            'h1',
            'h1.entry-title',
            'h1.post-title',
            '.article-title',
            '.post-title',
            'title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 0:
                    break
        
        # If no valid title found, return None
        if not title:
            return None
        
        # Try multiple selectors for content
        content = None
        content_selectors = [
            'article .entry-content',
            'article .post-content',
            'article .article-content',
            '.article-body',
            '.post-body',
            'article p',
            '.content p'
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                # Combine all paragraphs
                paragraphs = [elem.get_text(strip=True) for elem in elements if elem.get_text(strip=True)]
                if paragraphs:
                    content = ' '.join(paragraphs)
                    break
        
        # Fallback: get all text from article tag
        if not content:
            article_tag = soup.find('article')
            if article_tag:
                # Remove script and style elements
                for script in article_tag(["script", "style", "nav", "header", "footer"]):
                    script.decompose()
                content = article_tag.get_text(separator=' ', strip=True)
        
        # Validate content exists and has minimum length
        if not content or len(content) < 100:
            return None
        
        return {
            'url': article_url,
            'title': title,
            'content': content
        }

