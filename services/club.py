from models.club_model import Club
from repository.club import (get_clubs as repo_get_clubs,
                             update_clubs_in_json as repo_update_club_json)


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
        update_club(updated_club):
            Get the list of club, then in it replace the old club with
            the updated one.
        update_clubs_json(): Update both clubs list and clubs table in json.
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

    def update_clubs_list(self, club_to_update: Club) -> list[Club]:
        """
        Get the list of clubs, then in it replace the old club with
        the updated one.

        Returns:
            list[Club]:
                The updated list of clubs as Club objects.
        """
        clubs = repo_get_clubs()
        for i, club in enumerate(clubs):
            if club_to_update.club_name == club.club_name:
                index = i
                break
        clubs[index] = club_to_update
        return clubs

    def update_clubs_json(self, club_to_update: Club) -> None:
        """
        Update both clubs list and clubs table in json.

        Convert passed list of club objects into a list of dict,
        and call function to update json with converted list as arg.
        """
        clubs = self.update_clubs_list(club_to_update)
        repo_update_club_json([c.serialize_club() for c in clubs])
