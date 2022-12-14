from models.club_model import Club
from models.competition_model import Competition

from .competition import CompetitionService
from .club import ClubService


PLACE_COST = 3


class PurchaseHandler():
    """
    A class to represent a purchase instance.

    Attributes:
        club_name (str): The name of the club requesting purchase.
        competition_name (str):
            The name of the competition from which to purchase places.
        places_required (str): The number of places to purchase.
        comp_srv (CompetitionService):
            An instance of the CompetitionService class
        club_srv (ClubService):
            An instance of the ClubService class
        purchase_cost(int): The cost of the requested purchase.

    Methods:
        is_valid_places_required(places_required):
            Returns places_required as an integer.
        purchase_places(club, competition):
            Subtract purchase_cost from the points of the passed
            club and the number_of_places of the passed competition.
        execute_purchase(): Function to execute the purchase process.
        places_required_is_no_more_than_12():
            Check if the amount of places required
            to purchase doesn't exceed 12.
        is_valid_purchase(club, competition):
            Check all conditions for purchase.
    """
    def __init__(self, club_name: str, competition_name: str,
                 places_required: str, comp_service: CompetitionService,
                 club_service: ClubService) -> None:
        """
        Constructs all the necessary attributes for the PurchaseHandler object.

        Args:
            club_name (str): name of the club requesting booking.
            competition_name (str): competition requested to book.
            places_required (str): The number of places to purchase.
            comp_service (CompetitionService):
                An instance of the CompetitionService class
            club_service (ClubService): An instance of the ClubService class

        Raises:
            ValueError: If passed places_required cannot be converted into int.
        """
        self.club_name = club_name
        self.competition_name = competition_name
        self.club_srv = club_service
        self.comp_srv = comp_service
        self.places_required = self.is_valid_places_required(places_required)
        self.purchase_cost = self.places_required * PLACE_COST

    def is_valid_places_required(self, places_required: str) -> int:
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
            raise e

    def purchase_places(self, club: Club,
                        competition: Competition) -> tuple[Club, Competition]:
        """
        Subtract purchase_cost from the points of the passed
        club and the number_of_places of the passed competition.

        Args:
            club (Club): The club requesting the purchase.

            competition (Competition):
                The competition from which places are requested for purchase.

        Returns:
            tuple: club, competition as Club, Competition objects
        """
        competition.number_of_places -= self.purchase_cost
        club.points -= self.purchase_cost
        return club, competition

    def execute_purchase(self) -> dict:
        '''
        Function to execute the purchase process.

        It get the relevant club and competition from class attributes,
        validate the purchase, and if the purchase is valid,
        update their value in their respective lists.

        Returns:
            dict:
                A dict with the list of competitions,
                the club performing the purchase, and a message result.
                If purchase has been processed, return club
                and competitions with updated value.
                dict of: {'competitions': list[Competition],
                          'club': Club,
                          'msg': "Placeholder"}
        '''
        club = self.club_srv.get_club_by_name(self.club_name)
        competition = (
            self.comp_srv.get_competition_by_name(self.competition_name)
            )
        if self.is_valid_purchase(club, competition) is True:
            club, competition = self.purchase_places(club, competition)
            self.club_srv.update_clubs_json(club)
            self.comp_srv.update_competitions_json(competition)
            return {'competitions': self.comp_srv.get_competitions(),
                    'club': club,
                    'msg': f'Success-Purchased {self.places_required} places!'}
        else:
            return {'competitions': self.comp_srv.get_competitions(),
                    'club': club, 'msg': 'Cancelled-Invalid order'}

    def places_required_is_no_more_than_12(self) -> bool:
        """
        Check if the amount of places required to purchase
        doesn't exceed 12.

        Returns:
            bool: True if places doesn't exceed 12, False otherwise.
        """
        return True if self.places_required <= 12 else False

    def is_valid_purchase(self, club: Club,
                          competition: Competition) -> bool:
        """
        Check all conditions for purchase.

        Args:
            club (Club): The club requesting the purchase
            competition (Competition): The competition requested for purchase.

        Returns:
            bool: True if all conditions are met, False otherwise
        """
        is_valid = (True if
                    (self.club_srv.was_found(club)
                     and self.comp_srv.was_found(competition)
                     and competition.date_has_not_passed()
                     and competition.has_enough_places(self.places_required)
                     and self.places_required_is_no_more_than_12()
                     and club.has_enough_points(self.purchase_cost))
                    else False)
        return is_valid
