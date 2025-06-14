import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

def setup_database():
    load_dotenv()
    
    # Database connection parameters
    db_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', ''),
        'dbname': os.getenv('DB_NAME', 'sloelux_perf')
    }
    
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=db_params['host'],
            user=db_params['user'],
            password=db_params['password']
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Create database if it doesn't exist
        cur.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"), 
                   [db_params['dbname']])
        exists = cur.fetchone()
        if not exists:
            cur.execute(sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(db_params['dbname'])
            ))
            print(f"Database {db_params['dbname']} created successfully")
        
        # Connect to the new database
        conn.close()
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        # Create tables
        cur.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id SERIAL PRIMARY KEY,
                url VARCHAR(255) NOT NULL,
                lcp FLOAT,
                tbt FLOAT,
                inp VARCHAR(50),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS optimization_history (
                id SERIAL PRIMARY KEY,
                url VARCHAR(255) NOT NULL,
                issue_type VARCHAR(50),
                action_taken TEXT,
                before_metrics JSONB,
                after_metrics JSONB,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("Tables created successfully")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_database() 