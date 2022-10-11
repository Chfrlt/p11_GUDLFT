from repository.club import Club
from repository.competition import Competition

from .competition import CompetitionService
from .club import ClubService


class PurchaseHandler(CompetitionService, ClubService):

    def __init__(self, club: str, competition: str,
                 places_required: str) -> None:
        CompetitionService.__init__(self)
        ClubService.__init__(self)
        self.competition = None
        self.club = None
        self.places_required = self.is_valid_places_required(places_required)
        self.set_up(club, competition)

    def is_valid_places_required(self, places_required):
        try:
            return int(places_required)
        except ValueError:
            raise

    def set_up(self, club: str, competition: str) -> None:
        club = self.get_club_by_name(club)
        self.club = Club.deserialize_club(club)
        competition = self.get_competition_by_name(competition)
        self.competition = Competition.deserialize_competition(competition)

    def purchase_places(self) -> dict:
        self.competition.number_of_places -= self.places_required
        return {'competitions': self.competition.serialize_competition(),
                'club': self.club.serialize_club()}
