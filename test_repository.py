import unittest

from repository.club import Club
from repository.competition import Competition


class ClubTest(unittest.TestCase):

    def test_init_ok(self):
        club = Club('name', 10, 'example@email.com')
        self.assertEqual(club.club_name, 'name')
        self.assertEqual(club.email, 'example@email.com')
        self.assertEqual(club.points, 10)

    def test_init_bad_points_raises_value_error(self):
        with self.assertRaises(ValueError,
                               msg='Expected non int value'
                                   ' to raise an error'):
            Club('name', 'dix', 'example@email.com')

    def setUp(self) -> None:
        self.club = Club('name', 10, 'example@email.com')

    def test_serialize_club_returns_dict(self):
        club = self.club.serialize_club()
        self.assertIsInstance(club, dict,
                              msg='Expected club to be a dict')
        self.assertEqual(club['name'], self.club.club_name,
                         msg='Expected name value to be'
                             ' equal to self.club_name')
        self.assertEqual(club['email'], self.club.email,
                         msg='Expected email value to be'
                             ' equal to self.email')
        self.assertEqual(club['points'], self.club.points,
                         msg='Expected points value to be'
                             ' equal to self.points')

    def test_deserialize_club_returns_object(self):
        data = {'name': 'name', 'points': 10, 'email': 'example@email.com'}
        club = Club.deserialize_club(data)
        self.assertIsInstance(club, Club,
                              msg='Expected club to be'
                                  ' an instance of class Club')
        self.assertEqual(club.club_name, data['name'],
                         msg='Expected self.club_name to be'
                             ' equal to name value')
        self.assertEqual(club.email, data['email'],
                         msg='Expected self.email to be'
                             ' equal to email value')
        self.assertEqual(club.points, data['points'],
                         msg='Expected self.points to be'
                             ' equal to points value')


class CompetitionTest(unittest.TestCase):

    def test_init_ok(self):
        competition = Competition('name', '2020-03-27 10:00:00', 10)
        self.assertEqual(competition.competition_name, 'name')
        self.assertEqual(competition.date, '2020-03-27 10:00:00')
        self.assertEqual(competition.number_of_places, 10)

    def test_init_bad_number_of_places_raises_value_error(self):
        with self.assertRaises(ValueError,
                               msg='Expected non int value to raise an error'):
            Competition('name', '2020-03-27 10:00:00', 'dix')

    def setUp(self) -> None:
        self.competition = Competition('name', '2020-03-27 10:00:00', 10)

    def test_serialize_competition_returns_dict(self):
        competition = self.competition.serialize_competition()
        self.assertIsInstance(competition, dict,
                              'Expected competition to be a dict')
        self.assertEqual(competition['name'],
                         self.competition.competition_name,
                         msg=('Expected name value to be equal'
                              ' to self.competition_name'))
        self.assertEqual(competition['date'], self.competition.date,
                         msg=('Expected value of key date'
                              ' to be equal to competition.date'))
        self.assertEqual(competition['numberOfPlaces'],
                         self.competition.number_of_places,
                         msg=('Expected value of key numberOfPlaces'
                              ' to be equal to competition.number_of_places'))

    def test_deserialize_competition_returns_object(self):
        data = {'name': 'name',
                'date': '2020-03-27 10:00:00',
                'numberOfPlaces': 10}
        competition = Competition.deserialize_competition(data)
        self.assertIsInstance(competition, Competition,
                              msg='Expected competition to be'
                                  ' an instance of class competition')
        self.assertEqual(competition.competition_name, data['name'],
                         'Expected competition.competition_name'
                         ' to be equal to name value')
        self.assertEqual(competition.date, data['date'],
                         'Expected competition.date to be equal to date value')
        self.assertEqual(competition.number_of_places, data['numberOfPlaces'],
                         'Expected competition.number_of_places'
                         ' to be equal to numberOfPlaces value')


if __name__ == '__main__':
    unittest.main()
