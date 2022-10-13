from models.club_model import Club
from models.competition_model import Competition

from .competition import CompetitionService
from .club import ClubService


class PurchaseHandler():
    """
    A class to represent a purchase instance.

    Attributes:
        club_name (str): The name of the club requesting purchase.
        competition_name (str):
            The name of the competition from which to purchase places.
        places_required (str): The number of places to purchase.

    Methods:
        is_valid_places_required(places_required):
            Returns places_required as an integer.
        purchase_places(club, competition):
            Subtract attributes places_required from passed
            club points and passed competition number_of_places.
        execute_purchase(): Function to execute the purchase process.
    """
    def __init__(self, club_name: str, competition_name: str,
                 places_required: str) -> None:
        """
        Constructs all the necessary attributes for the PurchaseHandler object.

        Args:
            club_name (str): name of the club requesting booking.
            competition_name (str): competition requested to book.
            places_required (str): The number of places to purchase.

        Raises:
            ValueError: If passed places_required cannot be converted into int.
        """
        self.club_name = club_name
        self.competition_name = competition_name
        self.places_required = self.is_valid_places_required(places_required)

    def is_valid_places_required(self, places_required: str):
        """
        Returns places_required as an integer.

        Args:
            points (str): A string to be converted into an int.

        Returns:
            int: The passed points converted.

        Raises:
            ValueError: If passed points cannot be converted.
        """
        try:
            return int(places_required)
        except ValueError as e:
            print('Passed places_required to PurchaseHandler'
                  ' cannot be converted into int')
            raise e

    def purchase_places(self, club: Club,
                        competition: Competition) -> tuple[Club, Competition]:
        """
        Subtract attributes places_required from passed club and competition.

        Returns:
            tuple: club, competition as Club, Competition objects
        """
        competition.number_of_places -= self.places_required
        club.points -= self.places_required
        return club, competition

    def execute_purchase(self):
        '''
        Function to execute the purchase process.

        It get the relevant and club and competition from attributes,
        and update their value in their respectives list.

        Returns:
            dict:
                A dict with the list of competitions as objects and
                the updated club as objects.
                dict of: {'competitions': list[Competition], 'club': Club}
        '''
        club = ClubService().get_club_by_name(self.club_name)
        competition = (
            CompetitionService().get_competition_by_name(self.competition_name)
            )
        club_was_found = ClubService().was_found(club)
        comp_was_found = CompetitionService().was_found(competition)

        if club_was_found is True and comp_was_found is True:
            club, competition = self.purchase_places(club, competition)
            return {'competitions': CompetitionService().get_competitions(),
                    'club': club}
