import json

from models.club_model import Club

def load_clubs() -> list[Club]:
    """
    Function to load the clubs table in clubs.json.

    Returns:
        list[Club: object]:
            A list of clubs found in json as club objects.
    """
    list_ = []
    with open('clubs.json') as clubs:
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


get_clubs.all_clubs = []
