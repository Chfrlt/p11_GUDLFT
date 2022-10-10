from .competition import CompetitionService
from .club import ClubService


class BookingHandler(CompetitionService, ClubService):
    def __init__(self, club_name, competition_name) -> None:
        CompetitionService.__init__(self)
        ClubService.__init__(self)
        self.club_name = club_name
        self.competition_name = competition_name

    def find_data(self):
        found_club = ClubService().get_club_by_name(self.club_name)
        found_competition = (
            CompetitionService().get_competition_by_name(self.competition_name)
            )
        if self.is_valid_data(found_club, found_competition) is True:
            return {'competition': found_competition,
                    'club': found_club,
                    'message': None}
        else:
            return {'competition': self.competitions,
                    'club': self.club_name,
                    'message': 'Something went wrong-please try again'}

    def is_valid_data(self, club, competition):
        if club and competition:
            return True
        else:
            return False
