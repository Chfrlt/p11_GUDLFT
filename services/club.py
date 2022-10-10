from repository.club import Club


class ClubService():
    def __init__(self) -> None:
        self.clubs = Club.load_clubs()

    def get_club_by_email(self, email):
        return [club for club in self.clubs if club['email'] == email][0]

    def get_club_by_name(self, name):
        return [club for club in self.clubs if club['name'] == name][0]
