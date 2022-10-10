import json


class Club():

    def __init__(self, name, points, email) -> None:
        self.club_name = name
        self.email = email
        self.points = self.is_valid_points(points)
    
    
    def is_valid_points(points):
        try:
            return int(points)
        except ValueError:
            raise

    @classmethod
    def load_clubs(cls) -> list:
        with open('clubs.json') as c:
            clubs_list = json.load(c)['clubs']
            return clubs_list

    def serialize_club(self) -> dict:
        club = {'name': self.club_name,
                'email': self.email,
                'points': self.points}
        return club

    @classmethod
    def deserialize_club(cls, club: dict) -> object:
        c = Club(club['name'],
                 club['points'],
                 club['email'])
        return c
