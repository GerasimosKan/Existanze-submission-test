import sys

import requests


def get_character_data(character_name):
    url = f"https://swapi.dev/api/people/?search={character_name}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to retrieve data from the API.")
        return None

    return response.json()


# Display the character info
def display_character_info(character_data):
    if not character_data:
        print("The force is not strong within you.")
        return

    character = character_data[0]
    print(f"Name: {character['name']}")
    print(f"Height: {character['height']}")
    print(f"Mass: {character['mass']}")
    print(f"Birth Year: {character['birth_year']}")


# Search for a character
def search_character(character_name):
    data = get_character_data(character_name)

    if data and "results" in data:
        display_character_info(data["results"])


# handle command-line
def main():
    try:
        command, *args = sys.argv[1:]

        if command.lower() == "search" and args:
            character_name = " ".join(args)
            search_character(character_name)
        else:
            raise ValueError("Invalid command or missing character name.")
    except ValueError as e:
        print(f"Usage: python lemel1.py search <character name>  | Error: {e}")


if __name__ == "__main__":
    main()
