from supabase import create_client
import os
from dotenv import load_dotenv

def setup_tables():
    load_dotenv()
    
    # Initialize Supabase client
    supabase = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_SERVICE_KEY')  # Using service key for table creation
    )
    
    try:
        # Create performance_metrics table
        create_metrics_table = """
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id BIGSERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            lcp FLOAT,
            tbt FLOAT,
            inp TEXT,
            timestamp TIMESTAMPTZ DEFAULT NOW()
        );
        """
        
        # Create optimization_history table
        create_history_table = """
        CREATE TABLE IF NOT EXISTS optimization_history (
            id BIGSERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            issue_type TEXT NOT NULL,
            action_taken TEXT NOT NULL,
            before_metrics JSONB,
            after_metrics JSONB,
            timestamp TIMESTAMPTZ DEFAULT NOW()
        );
        """
        
        # Execute the SQL
        supabase.query(create_metrics_table).execute()
        supabase.query(create_history_table).execute()
        
        print("Tables created successfully!")
        
        # Enable RLS
        enable_rls = """
        ALTER TABLE performance_metrics ENABLE ROW LEVEL SECURITY;
        ALTER TABLE optimization_history ENABLE ROW LEVEL SECURITY;
        """
        supabase.query(enable_rls).execute()
        
        # Create policies
        create_policies = """
        CREATE POLICY "Allow read access to all users" ON performance_metrics
            FOR SELECT USING (true);
            
        CREATE POLICY "Allow read access to all users" ON optimization_history
            FOR SELECT USING (true);
        """
        supabase.query(create_policies).execute()
        
        print("RLS enabled and policies created!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_tables() 