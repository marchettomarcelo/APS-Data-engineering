"""
Simplified database utility functions for news aggregation pipeline.
Handles PostgreSQL connections and CRUD operations for 3 tables only.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Simplified database manager for news aggregation pipeline."""
    
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('POSTGRES_HOST', 'postgres'),
            'database': os.getenv('POSTGRES_DB', 'airflow'),
            'user': os.getenv('POSTGRES_USER', 'airflow'),
            'password': os.getenv('POSTGRES_PASSWORD', 'airflow'),
            'port': os.getenv('POSTGRES_PORT', '5432')
        }
    
    def get_connection(self):
        """Get database connection."""
        try:
            conn = psycopg2.connect(**self.connection_params)
            return conn
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None, fetch: bool = False):
        """Execute a SQL query."""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(query, params)
            
            if fetch:
                result = cursor.fetchall()
                return [dict(row) for row in result]
            else:
                conn.commit()
                return cursor.rowcount
                
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error executing query: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    # Email Recipients Methods
    
    def get_email_recipients(self) -> List[Dict[str, Any]]:
        """Get all email recipients."""
        query = "SELECT * FROM email_recipients ORDER BY name"
        return self.execute_query(query, fetch=True)
    
    def add_email_recipient(self, name: str, email: str) -> int:
        """Add a new email recipient."""
        query = """
        INSERT INTO email_recipients (name, email)
        VALUES (%s, %s)
        ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
        RETURNING id
        """
        result = self.execute_query(query, (name, email), fetch=True)
        return result[0]['id'] if result else None
    
    def remove_email_recipient(self, email: str) -> bool:
        """Remove an email recipient by email address."""
        query = "DELETE FROM email_recipients WHERE email = %s"
        try:
            self.execute_query(query, (email,))
            return True
        except Exception as e:
            logger.error(f"Error removing email recipient: {e}")
            return False
    
    # Articles Methods
    
    def get_all_articles(self, limit: int = None) -> List[Dict[str, Any]]:
        """Get all articles, optionally limited."""
        query = "SELECT * FROM articles ORDER BY id DESC"
        if limit:
            query += f" LIMIT {limit}"
        return self.execute_query(query, fetch=True)
    
    def get_article_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Get article by URL."""
        query = "SELECT * FROM articles WHERE url = %s"
        result = self.execute_query(query, (url,), fetch=True)
        return result[0] if result else None
    
    def insert_article(self, url: str, title: str = None, content: str = None) -> int:
        """Insert or update an article."""
        query = """
        INSERT INTO articles (url, title, content)
        VALUES (%s, %s, %s)
        ON CONFLICT (url) DO UPDATE SET
            title = COALESCE(EXCLUDED.title, articles.title),
            content = COALESCE(EXCLUDED.content, articles.content)
        RETURNING id
        """
        try:
            result = self.execute_query(query, (url, title, content), fetch=True)
            return result[0]['id'] if result else None
        except Exception as e:
            logger.error(f"Error inserting article: {e}")
            return None
    
    def update_article(self, url: str, title: str = None, content: str = None) -> bool:
        """Update an existing article."""
        query = """
        UPDATE articles
        SET title = COALESCE(%s, title),
            content = COALESCE(%s, content)
        WHERE url = %s
        """
        try:
            self.execute_query(query, (title, content, url))
            return True
        except Exception as e:
            logger.error(f"Error updating article: {e}")
            return False
    
    def delete_article(self, url: str) -> bool:
        """Delete an article by URL."""
        query = "DELETE FROM articles WHERE url = %s"
        try:
            self.execute_query(query, (url,))
            return True
        except Exception as e:
            logger.error(f"Error deleting article: {e}")
            return False
    
    # Email Content Methods
    
    def insert_email_content(self, subject: str, content: str) -> int:
        """Insert email content."""
        query = """
        INSERT INTO email_content (subject, content)
        VALUES (%s, %s)
        RETURNING id
        """
        result = self.execute_query(query, (subject, content), fetch=True)
        return result[0]['id'] if result else None
    
    def get_latest_email_content(self) -> Optional[Dict[str, Any]]:
        """Get the most recent email content."""
        query = "SELECT * FROM email_content ORDER BY created_at DESC LIMIT 1"
        result = self.execute_query(query, fetch=True)
        return result[0] if result else None
    
    def get_email_content_by_id(self, email_id: int) -> Optional[Dict[str, Any]]:
        """Get email content by ID."""
        query = "SELECT * FROM email_content WHERE id = %s"
        result = self.execute_query(query, (email_id,), fetch=True)
        return result[0] if result else None

# Global database manager instance
db = DatabaseManager()
