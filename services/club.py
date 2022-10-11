from repository.club import Club


class ClubService():
    def __init__(self) -> None:
        self.clubs = Club.load_clubs()

    def get_club_by_email(self, email: str) -> dict:
        club = [club for club in self.clubs if club['email'] == email]
        return {'club': club[0] if self.was_found(club) is True else club,
                'template': self.login_validation(self.was_found(club)),
                'message': None if self.was_found(club) is True
                else "Sorry, that email wasn't found"}

    def get_club_by_name(self, name):
        return [club for club in self.clubs if club['name'] == name][0]

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
