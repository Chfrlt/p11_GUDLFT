import json


class Competition():
    def __init__(self, name, date, number_of_places) -> None:
        self.competition_name = name
        self.date = date
        self.number_of_places = (
            self.is_valid_number_of_places(number_of_places)
            )

    def is_valid_number_of_places(self, number_of_places):
        try:
            return int(number_of_places)
        except ValueError:
            print('Invalid value')

    @classmethod
    def load_competitions(cls):
        with open('competitions.json') as comps:
            competitions_list = json.load(comps)['competitions']
            return competitions_list

    def serialize_competition(self):
        competition = {'name': self.competition_name,
                       'date': self.date,
                       'numberOfPlaces': self.number_of_places}
        return competition

    @classmethod
    def deserialize_competition(cls, competition: dict):
        c = Competition(competition['name'],
                        competition['date'],
                        competition['numberOfPlaces'])
        return c
