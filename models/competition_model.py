class Competition():
    """
    A class to represent a competition.

    Attributes:
        competition_name (str): name of the competition
        date (str): date of the competition
        number_of_places (str): places avalaible for purchase in competition

    Methods:
        is_valid_number_of_places(number_of_places):
            Returns passed number_of_places as an integer.
        serialize_competition(): Convert self into a dictionary.
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
        Object method to convert self into a dictionary.

        Returns:
            dict: self converted into dict.
        """
        competition = {'name': self.competition_name,
                       'date': self.date,
                       'numberOfPlaces': str(self.number_of_places)}
        return competition
