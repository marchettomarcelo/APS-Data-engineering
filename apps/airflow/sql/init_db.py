"""
Database initialization script for simplified news aggregation pipeline.
Creates 3 tables: email_recipients, articles, and email_content.
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_db_connection():
    """Get database connection using Airflow's default connection."""
    return psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow",
        port="5432"
    )

def create_tables():
    """Create all required tables for the simplified news pipeline."""
    
    # SQL statements for table creation
    create_tables_sql = """
    -- Email recipients table
    CREATE TABLE IF NOT EXISTS email_recipients (
        id SERIAL PRIMARY KEY,
        name VARCHAR(200) NOT NULL,
        email VARCHAR(200) NOT NULL UNIQUE
    );

    -- Articles table
    CREATE TABLE IF NOT EXISTS articles (
        id SERIAL PRIMARY KEY,
        url VARCHAR(500) NOT NULL UNIQUE,
        title TEXT,
        content TEXT
    );

    -- Email content table
    CREATE TABLE IF NOT EXISTS email_content (
        id SERIAL PRIMARY KEY,
        subject VARCHAR(500),
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url);
    CREATE INDEX IF NOT EXISTS idx_email_content_created_at ON email_content(created_at);
    """

    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Execute the SQL statements
        cursor.execute(create_tables_sql)
        
        print("✅ All tables created successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

def seed_initial_data():
    """Seed initial data for email recipients."""
    
    seed_data_sql = """
    -- Insert sample email recipients
    INSERT INTO email_recipients (name, email) VALUES 
    ('Marcelo Marchetto', 'marcelovfm@al.insper.edu.br')
    ON CONFLICT (email) DO NOTHING;
    """
    
    try:
        conn = get_db_connection()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute(seed_data_sql)
        
        print("✅ Initial data seeded successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        raise

if __name__ == "__main__":
    print("🚀 Initializing simplified news aggregation database...")
    create_tables()
    seed_initial_data()
    print("✅ Database initialization completed!")
