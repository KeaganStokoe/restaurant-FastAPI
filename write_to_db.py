import os
import supabase
from typing import Dict
from dotenv import load_dotenv


load_dotenv()


# Initialize the Supabase client with your project URL and API key
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

def write_establishment_to_supabase(new_data: Dict):
    # Convert all text in the new data to lowercase
    new_data = {key: value.lower() if isinstance(value, str) else value for key, 
                value in new_data.items()}

    # Insert the new data into your table
    table_name = "establishments"
    result, error = supabase_client.table(table_name).insert(new_data).execute()

    if error:
        print("An error occurred while writing to Supabase:", error)
    else:
        print("Data successfully written to Supabase:", result)