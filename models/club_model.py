class Club():
    """
    A class to represent a club.

    Attributes:
        club_name (str): name of the club
        email (str): email of the club
        points (int): points avalaible to the club

    Methods:
        is_valid_points(points):
            Returns passed points as an integer.
        serialize_club(): Convert self into a dictionary.
    """

    def __init__(self, club_dict: dict) -> None:
        """
        Constructs all the necessary attributes for the Club object.

        Args:
            club_dict (dict): A dict containing club infos.
                For example: {"name": "Simply Lift",
                              "email": "john@simplylift.co", "points": "9"}

        Raises:
            ValueError: If passed club_dict['points'] cannot be converted.
        """
        self.club_name = club_dict['name']
        self.email = club_dict['email']
        self.points = self.is_valid_points(club_dict['points'])

    def is_valid_points(self, points: str) -> int:
        """
        Returns passed points as an integer.

        Args:
            points (str): A string to be converted into an int.

        Returns:
            int: The passed points converted.

        Raises:
            ValueError: If passed points cannot be converted.
        """
        try:
            return int(points)
        except ValueError as e:
            print('Passed points to club model cannot be converted into int')
            raise e

    def serialize_club(self) -> dict:
        """
        Convert self into a dictionary.

        Returns:
            dict: self converted into dict.
        """
        club = {'name': self.club_name,
                'email': self.email,
                'points': str(self.points)}
        return club
