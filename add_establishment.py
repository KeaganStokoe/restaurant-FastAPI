from write_to_db import write_establishment_to_supabase
from langchain.tools import GooglePlacesTool
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GPLACES_API_KEY = os.environ.get("GPLACES_API_KEY")

def add_location(query):
    places = GooglePlacesTool()
    result = places.run(query)

    # Process the result string into a dictionary
    result_dict = process_result_string(result)

    # Write the dictionary data to the database
    write_establishment_to_supabase(result_dict)
    return True

def process_result_string(result_string):
    # Split the result string into lines
    lines = result_string.strip().split("\n")

    # Extract the data from the lines
    name = lines[0].split(".")[1].strip()
    address = lines[1].split(":")[1].strip()
    phone = lines[2].split(":")[1].strip()
    website_parts = lines[3].split(":")[1:]  # Join all parts after the colon
    website = ":".join(website_parts).strip()  # Join website parts with colons

    # Extract the opening hours as a list of strings
    try:
        opening_hours = lines[4].split(":")[1:]
        opening_hours = [oh.strip() for oh in opening_hours]
    except IndexError:
        opening_hours = "Unknown"

    # Extract the rating as a float value
    try:
        rating = float(lines[5].split(":")[1].strip())
    except (IndexError, ValueError):
        rating = "Unknown"

    # Extract the description as a string
    try:
        description = lines[6].split(":")[1].strip()
    except IndexError:
        description = "Unknown"

    # Create a dictionary with the extracted data
    result_dict = {
        "name": name,
        "address": address,
        "phone": phone,
        "website": website,
        "opening_hours": opening_hours,
        "rating": rating,
        "description": description
    }

    return result_dict