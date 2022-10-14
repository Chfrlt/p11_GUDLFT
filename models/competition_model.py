import datetime


class Competition():
    """
    A class to represent a competition.

    Attributes:
        competition_name (str): name of the competition
        date (str): date of the competition
        number_of_places (int): places avalaible for purchase in competition

    Methods:
        is_valid_number_of_places(number_of_places):
            Returns passed number_of_places as an integer.
        serialize_competition(): Convert self into a dictionary.
        has_enough_places(places_required):
            Check if the number of places avalaible is superior or
            equal to the passed number of places required.
        date_has_not_passed(): Check if the date of the competition has passed.
    """
    def __init__(self, comp_dict: dict) -> None:
        """
        Constructs all the necessary attributes for the competition object.

        Args:
            comp_dict (dict) : A dict containing competition info.
                For example: {"name": "Spring Festival",
                              "date": "2020-03-27 10:00:00",
                              "numberOfPlaces": "21"}

        Raises:
            ValueError:
                If passed comp_dict['NumberOfPlaces']
                cannot be converted into an int.
        """
        self.competition_name = comp_dict['name']
        self.date = comp_dict['date']
        self.number_of_places = (
            self.is_valid_number_of_places(comp_dict['numberOfPlaces']))

    def is_valid_number_of_places(self, number_of_places: str) -> int:
        """
        Returns passed number_of_places as an integer.

        Args:
            number_of_places (str): A string to be converted into an int.

        Returns:
            int: The passed number_of_places converted into an int.

        Raises:
            ValueError: If passed number_of_places cannot be converted.
        """
        try:
            return int(number_of_places)
        except ValueError as e:
            print('Passed number_of_places to competition'
                  ' model cannot be converted into int')
            raise e

    def serialize_competition(self):
        """
        Convert self into a dictionary.

        Returns:
            dict: self converted into dict.
        """
        competition = {'name': self.competition_name,
                       'date': self.date,
                       'numberOfPlaces': str(self.number_of_places)}
        return competition

    def date_has_not_passed(self) -> bool:
        """
        Check if the date of the competition has passed.

        Return:
            bool: True if competition has not passed, False otherwise
        """
        curr_time = datetime.datetime.now()
        competition_time = (
            datetime.datetime.strptime(self.date, "%Y-%m-%d %H:%M:%S"))
        return True if competition_time > curr_time else False

    def has_enough_places(self, places_requested: int) -> bool:
        """
        Check if the number of places avalaible is superior or
        equal to the passed number of places required.

        Args:
            places_required (int): The number of places requested.

        Returns:
            bool:
                True if number of places available is superior or equal
                to the amount of places required, False otherwise.
        """
        return True if self.number_of_places - places_requested >= 0 else False
