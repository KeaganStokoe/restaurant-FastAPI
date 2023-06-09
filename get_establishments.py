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

    # Execute query
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
            description = row.get('description', '-')
            if user_input.lower() in name.lower() or user_input in description.lower():
                # formatting the name
                formatted_name = ' '.join(word.capitalize() for word in name.split())
                # Collecting details
                description = row.get('description', '-')
                website = row.get('website', '-')
                # prepare and append search results
                search_result = f"{formatted_name}\n📝 Description: {description}\n🍽️  \n👾 Website: {website}\n"
                search_results.append(search_result)
        # fix the indentation of else statement
        final_string = "\n\n".join(search_results)
        return final_string