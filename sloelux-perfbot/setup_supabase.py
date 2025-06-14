from supabase import create_client
import os
from dotenv import load_dotenv

def setup_supabase():
    load_dotenv()
    
    # Initialize Supabase client
    supabase = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    try:
        # Create performance_metrics table using SQL
        supabase.query("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id BIGSERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                lcp FLOAT,
                tbt FLOAT,
                inp TEXT,
                timestamp TIMESTAMPTZ DEFAULT timezone('utc'::text, now())
            );
        """).execute()
        print("Created performance_metrics table")
        
        # Create optimization_history table using SQL
        supabase.query("""
            CREATE TABLE IF NOT EXISTS optimization_history (
                id BIGSERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                issue_type TEXT,
                action_taken TEXT,
                before_metrics JSONB,
                after_metrics JSONB,
                timestamp TIMESTAMPTZ DEFAULT timezone('utc'::text, now())
            );
        """).execute()
        print("Created optimization_history table")
        
        # Create RLS policies
        # Enable RLS
        supabase.query("""
            ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
            ALTER TABLE optimization_history ENABLE ROW LEVEL SECURITY;
        """).execute()
        
        # Create policies
        supabase.query("""
            CREATE POLICY "Allow read access to authenticated users" 
            ON performance_metrics FOR SELECT 
            TO authenticated 
            USING (true);
            
            CREATE POLICY "Allow read access to authenticated users" 
            ON optimization_history FOR SELECT 
            TO authenticated 
            USING (true);
        """).execute()
        
        print("Created RLS policies")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_supabase() 