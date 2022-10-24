import json
from pathlib import Path

from models.competition_model import Competition

filename_comp = (
    Path(__file__).parent.parent.absolute().joinpath('competitions.json'))

def load_competitions() -> list[Competition]:
    """
    Function to load the competitions table in competitions.json.

    Returns:
        list[Competition] :
            A list of competitions found in json as Competition objects.
    """
    list_ = []
    with open(filename_comp) as comps:
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


def update_competitions_in_json(updated_competitions: list[dict]) -> None:
    """
    Function to rewrite the competitions table in competitions.json with
    the updated competitions.

    Update the variable all_competitions with newly updated data.

    Args:
        updated_competitions list[dict]: A list of competition dicts
    """
    with open(filename_comp, 'w') as comps:
        dump = json.dumps({'competitions': updated_competitions})
        comps.write(dump)
    get_competitions.all_competitions = load_competitions()


get_competitions.all_competitions = []
