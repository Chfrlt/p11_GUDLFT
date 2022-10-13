from models.club_model import Club
from repository.club import get_clubs as repo_get_clubs


class ClubService():
    def __init__(self) -> None:
        pass

    def get_club_by_email(self, email: str) -> dict:
        club = [club for club in self.get_clubs() if club.email == email]
        print(club[0].serialize_club()['name'])
        return {'club': club[0].serialize_club() if self.was_found(club) is True else club,
                'template': self.login_validation(self.was_found(club)),
                'message': None if self.was_found(club) is True
                else "Sorry, that email wasn't found"}

    def get_club_by_name(self, name: str):
        club = [club for club in self.get_clubs() if club.club_name == name]
        return club[0].serialize_club() if self.was_found(club) is True else club

    def was_found(self, club: dict | None) -> bool:
        """
        Check if the passed club is not None.

        Arg:
            club (Club | None): The club to check.

        Returns:
            bool: True if club is not None, False otherwise.
        """
        if club:
            return True
        else:
            return False
    
    def login_validation(self, club_found: bool = False) -> str:
        if club_found is False:
            return 'index.html'
        else:
            return 'welcome.html'

    def get_clubs(self) -> list[Club]:
        """
        Get the list of clubs.

        Returns:
            list[Club]: A list of clubs as Club objects.
        """
        return repo_get_clubs()

    def was_found(self, club: list) -> bool:
        if club:
            return True
        else:
            return False

    def login_validation(self, club_found: bool = False) -> str:
        if club_found is False:
            return 'index.html'
        else:
            return 'welcome.html'
