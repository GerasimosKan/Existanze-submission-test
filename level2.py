import sys

import requests


def get_character_data(character_name):
    url = f"https://swapi.dev/api/people/?search={character_name}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve data from the API.")
        return None

    return response.json()


def get_homeworld_data(homeworld_url):
    response = requests.get(homeworld_url)

    if response.status_code != 200:
        print("Failed to retrieve homeworld data.")
        return None

    return response.json()


# Function to display character info
def display_character_info(character_data, homeworld_data=None):
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

        # orbital and rotation
        orbital_period = float(homeworld_data["orbital_period"])
        rotation_period = float(homeworld_data["rotation_period"])

        # Calculate the Earth years and days
        earth_orbital_period = 365.25
        earth_rotation_period = 24

        homeworld_earth_years = orbital_period / earth_orbital_period
        homeworld_earth_days = rotation_period / earth_rotation_period

        print(
            f"On {homeworld_data['name']}, 1 year on earth is {homeworld_earth_years:.2f} years and 1 day is {homeworld_earth_days:.2f} days. "
        )


# Function to search for a character
def search_character(character_name, world_option=False):
    data = get_character_data(character_name)

    if data and "results" in data and data["results"]:
        character = data["results"]

        # Display character info
        display_character_info(character)

        # If the world option is provided, fetch homeworld data
        if world_option and "homeworld" in character[0]:
            homeworld_url = character[0]["homeworld"]
            homeworld_data = get_homeworld_data(homeworld_url)
            if homeworld_data:
                display_character_info(character, homeworld_data)
    else:
        print(f"No character found for '{character_name}'.")


# Handle command-line arguments
def main():
    try:
        # Parse the arguments correctly
        command, *args = sys.argv[1:]

        # Check if the '--world' flag is present
        world_option = "--world" in args
        # Remove the '--world' option from args if present
        if world_option:
            args.remove("--world")

        if command.lower() == "search" and args:
            character_name = " ".join(args)
            search_character(character_name, world_option)
        else:
            raise ValueError("Invalid command or missing character name.")
    except ValueError as e:
        print(
            f"Usage: python level2.py search <character name> [--world]\n" f"Error: {e}"
        )


if __name__ == "__main__":
    main()
