import os
from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()


# Initialize the Supabase client with your project URL and API key
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_establishments(user_input: str) -> str:
    """
    Searches the `establishments` table in Supabase using a simple string search based on the user's input.

    Args:
        user_input: A string representing the user's search query.

    Returns:
        A string representing the establishments that match the search query, formatted as a numbered list.
    """

    # Get all rows from the `establishments` table
    response = supabase_client.table("establishments").select('*').execute()

    # Check for errors and return the search results
    if len(response.data) < 1:
        print("No matches found")
        return "No matches found"
    else:
        rows = response.data
        search_results = []
        for i, row in enumerate(rows):
            # search the name using user input
            name = row.get('name', '-')
            if user_input.lower() in name.lower():
                # formatting the name
                formatted_name = ' '.join(word.capitalize() for word in name.split())
                # Collecting details
                description = row.get('description', '-')
                cuisine = ', '.join(row.get('cuisines', [])) or '-'
                website = row.get('website', '-')
                opening_hours = row.get('opening_hours', {}) or {}
                days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                # prepare and append search results
                search_result = f"{i+1}. {formatted_name}\n📝 Description: {description}\n🍽️ Cuisine: {cuisine.capitalize()}\n👾 Website: {website}\n"
                search_results.append(search_result)
        # fix the indentation of else statement
        final_string = "\n\n".join(search_results)
        return final_string