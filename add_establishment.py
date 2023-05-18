from write_to_db import write_establishment_to_supabase
from langchain.tools import GooglePlacesTool
from langchain.tools import DuckDuckGoSearchRun
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GPLACES_API_KEY = os.environ.get("GPLACES_API_KEY")

def add_location(query):
    places = GooglePlacesTool()
    result = places.run(query)
    description = get_location_description(query)

    # Process the result string into a dictionary
    result_dict = process_result_string(result, description)

    # Write the dictionary data to the database
    write_establishment_to_supabase(result_dict)
    return True

def get_location_description(establishment_name):
    search = DuckDuckGoSearchRun()
    description = search.run(f"{establishment_name} budapest description")
    return description

def process_result_string(result_string, description):
    # Split the result string into lines
    lines = result_string.strip().split("\n")

    # Extract the data from the lines
    name = lines[0].split(".")[1].strip()
    address = lines[1].split(":")[1].strip()
    phone = lines[2].split(":")[1].strip()
    website_parts = lines[3].split(":")[1:]  # Join all parts after the colon
    website = ":".join(website_parts).strip()  # Join website parts with colons

    # Create a dictionary with the extracted data
    result_dict = {
        "name": name,
        "description": description,
        "address": address,
        "phone": phone,
        "website": website,
    }

    return result_dict