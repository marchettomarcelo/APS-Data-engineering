"""
Simplified News Aggregation Pipeline DAG.
Scrapes news articles, generates email content with AI, and sends to recipients.
"""

from __future__ import annotations

import pendulum
import logging
from datetime import timedelta
from typing import List, Dict, Any

from airflow.models.dag import DAG
from airflow.decorators import task
from airflow.exceptions import AirflowException

# Import our custom utilities
import sys
sys.path.append('/opt/airflow/dags')

from utils.db_utils import db
from utils.scraper import Scraper
from utils.llm_utils import get_email_generator
from utils.email_utils import get_email_manager
from sql.init_db import create_tables, seed_initial_data

logger = logging.getLogger(__name__)

# DAG configuration
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': pendulum.datetime(2024, 1, 1, tz="UTC"),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Hardcoded news sources
NEWS_SOURCES = [
    {"name": "IstoÉDinheiro", "url": "https://www.istoedinheiro.com.br/"},
    {"name": "MoneyTimes", "url": "https://moneytimes.com.br/"}
]

# Create DAG
with DAG(
    dag_id="news_pipeline_dag",
    default_args=default_args,
    description="Simplified news aggregation and email pipeline",
    schedule="0 8 * * *",  # Daily at 8:00 AM UTC
    catchup=False,
    tags=["news", "scraping", "ai", "email"],
    max_active_runs=1,
) as dag:

    @task
    def initialize_database():
        """Initialize database tables and seed initial data."""
        try:
            logger.info("Creating database tables...")
            create_tables()
            logger.info("Seeding initial data...")
            seed_initial_data()
            logger.info("Database initialization complete")
            return True
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise AirflowException(f"Failed to initialize database: {e}")

    @task
    def scrape_news():
        """Scrape articles from hardcoded news sources and store in database."""
        scraped_articles = []
        max_articles_per_source = 5
        
        for source in NEWS_SOURCES:
            source_name = source['name']
            source_url = source['url']
            
            try:
                logger.info(f"Scraping {source_name} - {source_url}")
                
                # Create scraper and fetch homepage
                scraper = Scraper(source_name, source_url)
                response = scraper.fetch_page(source_url)
                
                if not response:
                    logger.warning(f"Failed to fetch {source_name}")
                    continue
                
                # Extract article links
                article_links = scraper.extract_article_links(response.text)
                logger.info(f"Found {len(article_links)} articles on {source_name}")
                
                # Limit articles per source
                article_links = article_links[:max_articles_per_source]
                
                # Scrape each article
                for article_url in article_links:
                    try:
                        logger.info(f"Scraping article: {article_url}")
                        
                        # Fetch article page
                        article_response = scraper.fetch_page(article_url)
                        if not article_response:
                            continue
                        
                        # Extract article data
                        article_data = scraper.extract_article_data(
                            article_response.text, 
                            article_url
                        )
                        
                        # Skip article if no valid data was extracted
                        if not article_data:
                            logger.warning(f"Skipping article (no valid title or content): {article_url}")
                            continue
                        
                        # Store in database
                        article_id = db.insert_article(
                            url=article_url,
                            title=article_data['title'],
                            content=article_data['content']
                        )
                        
                        if article_id:
                            scraped_articles.append({
                                'id': article_id,
                                'url': article_url,
                                'title': article_data['title'],
                                'content': article_data['content']
                            })
                            logger.info(f"Stored article: {article_data['title'][:50]}...")
                        
                    except Exception as e:
                        logger.error(f"Error scraping article {article_url}: {e}")
                        continue
                
            except Exception as e:
                logger.error(f"Error scraping {source_name}: {e}")
                continue
        
        logger.info(f"Scraping complete: {len(scraped_articles)} articles collected")
        return scraped_articles

    @task
    def generate_email(scraped_articles: List[Dict[str, Any]]):
        """Generate email content using LLM and store in database."""
        
        if not scraped_articles:
            logger.warning("No articles to generate email from")
            return None
        
        try:
            # Get email generator
            generator = get_email_generator()
            
            # Generate email content (subject + HTML body)
            email_data = generator.generate_email_content(scraped_articles)
            
            # Store in database
            email_id = db.insert_email_content(
                subject=email_data['subject'],
                content=email_data['content']
            )
            
            logger.info(f"Generated email content with ID: {email_id}")
            
            return {
                'email_id': email_id,
                'subject': email_data['subject'],
                'content': email_data['content'],
                'article_count': len(scraped_articles)
            }
            
        except Exception as e:
            logger.error(f"Error generating email content: {e}")
            raise AirflowException(f"Failed to generate email: {e}")

    @task
    def send_emails(email_data: Dict[str, Any]):
        """Send email to all recipients in the database."""
        
        if not email_data:
            logger.warning("No email data to send")
            return {"emails_sent": 0, "errors": []}
        
        try:
            # Get all email recipients
            recipients = db.get_email_recipients()
            
            if not recipients:
                logger.warning("No email recipients found in database")
                return {"emails_sent": 0, "errors": ["No recipients found"]}
            
            logger.info(f"Sending email to {len(recipients)} recipients")
            
            # Get email manager
            email_manager = get_email_manager()
            
            # Send emails
            results = email_manager.send_email(
                subject=email_data['subject'],
                content=email_data['content'],
                recipients=recipients
            )
            
            logger.info(f"Email sending complete: {results['success_count']} sent, {results['failed_count']} failed")
            
            return {
                'emails_sent': results['success_count'],
                'emails_failed': results['failed_count'],
                'details': results['details']
            }
            
        except Exception as e:
            logger.error(f"Error sending emails: {e}")
            raise AirflowException(f"Failed to send emails: {e}")

    # Define task dependencies (4-step pipeline with DB initialization)
    db_init = initialize_database()
    articles = scrape_news()
    email_content = generate_email(articles)
    email_results = send_emails(email_content)
    
    # Set up task flow
    db_init >> articles >> email_content >> email_results
