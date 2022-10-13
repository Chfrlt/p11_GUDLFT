import json

from models.competition_model import Competition


def load_competitions() -> list[Competition]:
    """
    Function to load the competitions table in competitions.json.

    Returns:
        list[Competition: object] :
            A list of competitions found in json as Competition objects.
    """
    list_ = []
    with open('competitions.json') as comps:
        competitions_list = json.load(comps)['competitions']
        for comp in competitions_list:
            list_.append(Competition(comp))
        return list_


def get_competitions() -> list[Competition]:
    """
    Function to get the list of competitions.

    If competitions were not loaded into
    variable all_competition yet, load them.

    Returns:
        list[Competition]:
            Variable all_competitions set as a list of Competition objects.
    """
    if not get_competitions.all_competitions:
        get_competitions.all_competitions = load_competitions()
    return get_competitions.all_competitions


get_competitions.all_competitions = []
