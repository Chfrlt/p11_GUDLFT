from repository.competition import Competition
from repository.competition import (get_competitions
                                    as repo_get_competitions)


class CompetitionService():
    def __init__(self) -> None:
        pass

    def get_competition_by_name(self, name: str) -> dict | None:
        """
        Find corresponding competition from passed name.

        Arg:
            name (str): The name of the requested competition

        Returns:
            Competition: Found competition as object if competition was found.
            None: If competition wasn't found.
        """
        comp = [comp for comp in repo_get_competitions()
                if comp.competition_name == name]
        return comp[0].serialize_competition() if self.was_found(comp) else None


    def was_found(self, competition: Competition | None) -> bool:
        """
        Check if the passed competition is not None.

        Arg:
            competition (Competition | None): The competition to check.

        Returns:
            bool: True if competition is not None, False otherwise.
        """
        if competition:
            return True
        else:
            return False

    def get_competitions(self):
        """
        Get the list of competitions.

        Returns:
            list[Competition]: A list of competitions as Competition objects.
        """
        return [comp.serialize_competition() for comp in repo_get_competitions()]
