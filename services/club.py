from models.club_model import Club
from repository.club import get_clubs as repo_get_clubs


class ClubService():
    """
    A class to handle service level action involving clubs.

    Methods:
        get_club_by_email(email): Find corresponding club from passed email.
        get_club_by_name(name): Find corresponding club from passed name.
        was_found(club): Check if the passed club is not None.
        get_clubs(): Get the list of clubs.
        get_club_login_result(club_email):
            Determinate which template should user be redirected to
            by checking if passed email is associated with a registered email.
    """
    def __init__(self) -> None:
        pass

    def get_club_by_email(self, email: str) -> dict:
        """
        Find corresponding club from passed email.

        Arg:
            email (str): The email of the requested club.

        Returns:
            Club: Found club as object if club was found.
            None: If club wasn't found.
        """
        club = [club for club in repo_get_clubs() if club.email == email]
        return club[0] if self.was_found(club) is True else None

    def get_club_by_name(self, name: str) -> Club | None:
        """
        Find corresponding club from passed name.

        Arg:
            name (str): The name of the requested club

        Returns:
            Club: Found club as object if club was found.
            None: If club wasn't found.
        """
        club = [club for club in repo_get_clubs() if club.club_name == name]
        return club[0] if self.was_found(club) is True else None

    def was_found(self, club: Club | None) -> bool:
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

    def get_club_login_result(self, club_email: str) -> dict:
        '''
        Determinate which template should user be redirected to
        by checking if passed email is associated with a registered email.

        Arg:
            club_email (str): email attempting login with.

        Returns:
            dict: {'template': 'welcome.html', 'club': club, 'msg': None}
                If club was found.
            dict: {'template': 'index.html', 'club': club,
                   'msg': "Sorry, that email wasn't found"}
                If club wasn't found.
        '''
        club = self.get_club_by_email(club_email)
        club_was_found = self.was_found(club)
        if club_was_found is True:
            return {'template': 'welcome.html',
                    'club': club,
                    'msg': None}
        if club_was_found is False:
            return {'template': 'index.html',
                    'club': club,
                    'msg': "Sorry, that email wasn't found"}

    def get_clubs(self) -> list[Club]:
        """
        Get the list of clubs.

        Returns:
            list[Club]: A list of clubs as Club objects.
        """
        return repo_get_clubs()