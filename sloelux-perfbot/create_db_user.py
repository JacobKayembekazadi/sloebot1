import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

def create_db_user():
    load_dotenv()
    
    # New user credentials
    new_user = "sloelux_user"
    new_password = "sloelux_password123"  # You should change this to a secure password
    db_name = "sloelux_perf"
    
    try:
        # Connect to PostgreSQL server as superuser
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres"  # Default password, change if different
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Create new user
        cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
            sql.Identifier(new_user)
        ), [new_password])
        print(f"User {new_user} created successfully")
        
        # Create database
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(db_name)
        ))
        print(f"Database {db_name} created successfully")
        
        # Grant privileges
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
            sql.Identifier(db_name),
            sql.Identifier(new_user)
        ))
        print(f"Privileges granted to {new_user}")
        
        # Connect to the new database to grant schema privileges
        conn.close()
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="postgres",
            dbname=db_name
        )
        cur = conn.cursor()
        
        # Grant schema privileges
        cur.execute(sql.SQL("GRANT ALL ON SCHEMA public TO {}").format(
            sql.Identifier(new_user)
        ))
        print("Schema privileges granted")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
            
    # Update .env file with new credentials
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as file:
            lines = file.readlines()
        
        with open(env_path, 'w') as file:
            for line in lines:
                if line.startswith('DB_USER='):
                    file.write(f'DB_USER={new_user}\n')
                elif line.startswith('DB_PASSWORD='):
                    file.write(f'DB_PASSWORD={new_password}\n')
                elif line.startswith('DB_NAME='):
                    file.write(f'DB_NAME={db_name}\n')
                else:
                    file.write(line)
        print(".env file updated with new credentials")

if __name__ == "__main__":
    create_db_user() 