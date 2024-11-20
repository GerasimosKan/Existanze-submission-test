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
    return {}


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

    if character_name in cache:
        cached_data = cache[character_name]
        if world_option and cached_data.get("homeworld_data"):
            print(f"Using cached data for '{character_name}' with homeworld...")
            display_character_info(
                cached_data["character_data"],
                cached_data["homeworld_data"],
                cached_data["timestamp"],
            )
            return
        elif not world_option:
            print(f"Using cached data for '{character_name}'...")
            display_character_info(
                cached_data["character_data"], None, cached_data["timestamp"]
            )
            return

    # Fetch data from the API
    data = get_character_data(character_name)
    if data and "results" in data and data["results"]:
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
    else:
        print(f"No character found for '{character_name}'.")


# Clean the cache
def clean_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
        print("Cache has been removed. 😎")
    else:
        print("No cache file found.")


# Handle command-line arguments
def main():
    try:
        command, *args = sys.argv[1:]
        world_option = "--world" in args
        if world_option:
            args.remove("--world")

        if command.lower() == "search" and args:
            character_name = " ".join(args)
            search_character(character_name, world_option)

        elif command.lower() == "cache" and args and args[0] == "--clean":
            clean_cache()

        else:
            raise ValueError("Invalid command or missing character name.")
    except ValueError as e:
        print(
            f"Usage: python level3.py search <character name> [--world]\n"
            f"       python level3.py cache --clean\n"
            f"Error: {e}"
        )


if __name__ == "__main__":
    main()
