from supabase import create_client
import os
from dotenv import load_dotenv

def test_supabase_connection():
    load_dotenv()
    
    # Print environment variables (without sensitive data)
    print("SUPABASE_URL:", os.getenv('SUPABASE_URL'))
    print("SUPABASE_KEY exists:", bool(os.getenv('SUPABASE_KEY')))
    
    # Initialize Supabase client
    supabase = create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )
    
    try:
        # Just try to select from the table
        result = supabase.table('performance_metrics').select('*').limit(1).execute()
        print("\nConnection successful!")
        print("Data:", result.data)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease check:")
        print("1. Your Supabase URL and key are correct")
        print("2. The table 'performance_metrics' exists")
        print("3. RLS policies allow reading from the table")
        print("4. Your network can reach Supabase")

if __name__ == "__main__":
    test_supabase_connection() 