import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "news_agent.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            source TEXT,
            published_date TEXT,
            category TEXT,
            clean_text TEXT
        )
    ''')
    
    # Metrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_type TEXT,
            value TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # Query logs table for tracking RAG queries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            mode TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def log_query(query, mode="rag"):
    """Log a user query for metrics tracking"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO query_logs (query, mode) VALUES (?, ?)', (query, mode))
    conn.commit()
    conn.close()

def get_article_count():
    """Get total number of articles in database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM articles')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_query_count():
    """Get total number of queries processed"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM query_logs')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_recent_queries(limit=10):
    """Get recent queries"""
    conn = get_db_connection()
    df = pd.read_sql(f'SELECT * FROM query_logs ORDER BY timestamp DESC LIMIT {limit}', conn)
    conn.close()
    return df

def save_articles(df):
    conn = get_db_connection()
    # Ensure columns match
    # We might need to map dataframe columns to table columns
    # For now, let's assume df has 'title', 'content', 'source', 'published_date', 'category', 'clean_text'
    
    # Select only relevant columns if they exist
    cols = ['title', 'content', 'source', 'published_date', 'category', 'clean_text']
    available_cols = [c for c in cols if c in df.columns]
    
    df[available_cols].to_sql('articles', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Saved {len(df)} articles to database.")

def get_articles():
    conn = get_db_connection()
    df = pd.read_sql('SELECT * FROM articles', conn)
    conn.close()
    return df

def save_setting(key, value):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def get_setting(key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    return row['value'] if row else None
