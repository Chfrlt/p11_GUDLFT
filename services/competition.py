from repository.competition import Competition
from repository.competition import (get_competitions
                                    as repo_get_competitions)


class CompetitionService():
    def __init__(self) -> None:
        pass

    def get_competition_by_name(self, name):
        return [comp for comp in self.get_competitions() if comp['name'] == name][0]

    def get_competitions(self):
        """
        Get the list of competitions.

        Returns:
            list[Competition]: A list of competitions as Competition objects.
        """
        return [comp.serialize_competition() for comp in repo_get_competitions()]
