import json
import os
import sys
from datetime import datetime

import requests

CACHE_FILE = "cache.json"


# Load cache from the file
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as cache_file:
            return json.load(cache_file)
    return {"search_history": []}  # Default to an empty search history


# Save cache to the file
def save_cache(cache_data):
    with open(CACHE_FILE, "w") as cache_file:
        json.dump(cache_data, cache_file, indent=4)


# Get character data from the API
def get_character_data(character_name):
    url = f"https://swapi.dev/api/people/?search={character_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        print("Failed to retrieve character data from the API.")
        return None


# Get homeworld data from the API
def get_homeworld_data(homeworld_url):
    try:
        response = requests.get(homeworld_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        print("Failed to retrieve homeworld data from the API.")
        return None


# Display character information
def display_character_info(character_data, homeworld_data=None, cached_time=None):
    if not character_data:
        print("The force is not strong within you.")
        return

    character = character_data[0]
    print(f"Name: {character['name']}")
    print(f"Height: {character['height']}")
    print(f"Mass: {character['mass']}")
    print(f"Birth Year: {character['birth_year']}")

    if homeworld_data:
        print("\nHomeworld")
        print("----------------")
        print(f"Name: {homeworld_data['name']}")
        print(f"Population: {homeworld_data['population']}")

        orbital_period = float(homeworld_data["orbital_period"])
        rotation_period = float(homeworld_data["rotation_period"])

        earth_orbital_period = 365.25
        earth_rotation_period = 24

        homeworld_earth_years = orbital_period / earth_orbital_period
        homeworld_earth_days = rotation_period / earth_rotation_period

        print(
            f"On {homeworld_data['name']}, 1 year on Earth is {homeworld_earth_years:.2f} years "
            f"and 1 day is {homeworld_earth_days:.2f} days."
        )

    if cached_time:
        cached_time_obj = datetime.fromisoformat(cached_time)
        formatted_time = cached_time_obj.strftime("%d-%m-%Y %H:%M:%S")
        print(f"\nCached at: {formatted_time}")


# Perform a character search
def search_character(character_name, world_option=False):
    cache = load_cache()
    search_result = "Failure"

    # Check if the character was searched recently
    if character_name in cache:
        cached_data = cache[character_name]
        if world_option and cached_data.get("homeworld_data"):
            print(f"Using cached data for '{character_name}' with homeworld...")
            display_character_info(
                cached_data["character_data"],
                cached_data["homeworld_data"],
                cached_data["timestamp"],
            )
            search_result = "Success"
        elif world_option and not cached_data.get("homeworld_data"):
            search_result = fetchDataFromApi(character_name, world_option, cache)
        elif not world_option:
            print(f"Using cached data for '{character_name}'...")
            display_character_info(
                cached_data["character_data"], None, cached_data["timestamp"]
            )
            search_result = "Success"
        else:
            search_result = "Failure"
    else:
        search_result = fetchDataFromApi(character_name, world_option, cache)

    # Log search to the history
    cache["search_history"].append(
        {
            "character_name": character_name,
            "result": search_result,
            "timestamp": datetime.now().isoformat(),
        }
    )
    save_cache(cache)


# Fetch data from the API
def fetchDataFromApi(character_name, world_option, cache):
    data = get_character_data(character_name)
    if data and "results" in data:
        character = data["results"]

        homeworld_data = None
        if world_option and "homeworld" in character[0]:
            homeworld_url = character[0]["homeworld"]
            homeworld_data = get_homeworld_data(homeworld_url)

        display_character_info(character, homeworld_data)

        # Cache the results
        timestamp = datetime.now().isoformat()
        cache[character_name] = {
            "character_data": character,
            "homeworld_data": homeworld_data,
            "timestamp": timestamp,
        }
        save_cache(cache)
        return "Success"
    else:
        print(
            f"No data found or results in the API response for the '{character_name}'."
        )
        return "Failure"


# Clean the cache
def clean_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("Cache has been removed.")
    else:
        print("No cache file found.")


# Display search history
def display_search_history():
    cache = load_cache()
    search_history = cache.get("search_history", [])

    if not search_history:
        print("No search history available.")
        return

    print(f"\n{'Search Term':<25}{'Result':<10}{'Timestamp'}")
    print("-" * 60)
    for entry in search_history:
        search_time = datetime.fromisoformat(entry["timestamp"]).strftime(
            "%d-%m-%Y %H:%M:%S"
        )
        print(f"{entry['character_name']:<25}{entry['result']:<10}{search_time}")


# Handle command-line arguments
def main():
    try:
        command, *args = sys.argv[1:]
        world_option = "--world" in args
        if world_option:
            args.remove("--world")

        if command.lower() == "search" and args:
            character_name = " ".join(args).strip("'")
            search_character(character_name, world_option)

        elif command.lower() == "cache" and args:
            if args[0] == "--clean":
                clean_cache()
            elif args[0] == "--history":
                display_search_history()
            else:
                print("Invalid cache command.")

        else:
            raise ValueError("Invalid command or missing character name.")
    except ValueError as e:
        print(
            f"Usage: python main.py search <character name> [--world]\n"
            f"       python main.py cache --clean\n"
            f"       python main.py cache --history\n"
            f"Error: {e}"
        )


if __name__ == "__main__":
    main()
