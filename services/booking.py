from .competition import CompetitionService
from .club import ClubService


class BookingHandler():
    """
    A class to represent a booking instance.

    Attributes:
        club_name (str): name of the club requesting booking
        competition_name (int): competition requested to book
        comp_srv (CompetitionService):
            An instance of the CompetitionService class
        club_srv (ClubService):
            An instance of the ClubService class

    Methods:
        find_booking_data():
            Returns a dict of corresponding objects from attributes.
    """
    def __init__(self, club_name: str, competition_name: str,
                 comp_service: CompetitionService,
                 club_service: ClubService) -> None:
        """
        Constructs all the necessary attributes for the BookingHandler object.

        Args:
            club_name (str): name of the club requesting booking.
            competition_name (str): competition requested to book.
            comp_service (CompetitionService):
                An instance of the CompetitionService class
            club_service (ClubService): An instance of the ClubService class
        """
        self.club_name = club_name
        self.competition_name = competition_name
        self.club_srv = club_service
        self.comp_srv = comp_service

    def find_booking_data(self) -> dict:
        """
        Returns a dict of corresponding objects from attributes.

        Gets Club object from attribute club_name.
        Gets Competition object from attribute competition_name.

        Returns:
            dict: A dict with the club and the competition found as objects.
                Dict of {
                    "competition": <competition found as Competition object>,
                    "club": <club found as Club object>
                    }
        """
        club = self.club_srv.get_club_by_name(self.club_name)
        comp = (
            self.comp_srv.get_competition_by_name(self.competition_name)
            )
        club_was_found = self.club_srv.was_found(club)
        comp_was_found = self.comp_srv.was_found(comp)
        if club_was_found is True and comp_was_found is True:
            return {'competition': comp,
                    'club': club}
