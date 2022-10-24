import json
from pathlib import Path

from models.club_model import Club

filename_club = (Path(__file__).parent.parent.absolute().joinpath('clubs.json'))

def load_clubs() -> list[Club]:
    """
    Function to load the clubs table in clubs.json.

    Arg:
        filename (str): The path to the json file containing data.

    Returns:
        list[Club: object]:
            A list of clubs found in json as club objects.
    """
    list_ = []
    with open(filename_club) as clubs:
        clubs_list = json.load(clubs)['clubs']
        for c in clubs_list:
            list_.append(Club(c))
        return list_


def get_clubs():
    """
    Function to get the list of clubs.

    If clubs were not loaded into
    variable all_clubs yet, load them.

    Returns:
        list[Club]:
            Variable all_clubs as a list of Club objects.
    """
    if not get_clubs.all_clubs:
        get_clubs.all_clubs = load_clubs()
    return get_clubs.all_clubs


def update_clubs_in_json(updated_clubs: list[dict]):
    """
    Function to rewrite the clubs table in clubs.json with
    the updated clubs.

    Update the variable all_clubs with newly updated data.

    Args:
        updated_clubs list[dict]: A list of the clubs as dicts
        filename (str): The path to the json file containing data.
    """
    with open(filename_club, 'w') as clubs:
        dump = json.dumps({'clubs': updated_clubs})
        clubs.write(dump)
    get_clubs.all_clubs = load_clubs()


get_clubs.all_clubs = []
