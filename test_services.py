import unittest

from services.competition import CompetitionService
from services.club import ClubService
from services.purchase import PurchaseHandler


class ClubServicesTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cs = ClubService()
        self.cs.clubs = [
            {'name': 'Club 01',
             'email': 'club01@opclassroom.co',
             'points': '10'},
            {'name': 'Club 02',
             'email': 'club02@opclassroom.com',
             'points': '20'}]

    def test_get_club_by_email_returns_club_dict(self):
        email = 'club01@opclassroom.co'
        expected_output = {
            'name': 'Club 01',
            'email': 'club01@opclassroom.co',
            'points': '10'}
        actual_outpout = self.cs.get_club_by_email(email)
        self.assertEqual(actual_outpout, expected_output,
                         msg='Expected club to be returned as a dict')

    def test_get_club_by_name_returns_club_dict(self):
        name = 'Club 02'
        expected_output = {
            'name': 'Club 02',
            'email': 'club02@opclassroom.com',
            'points': '20'}
        actual_outpout = self.cs.get_club_by_name(name)
        self.assertEqual(actual_outpout, expected_output,
                         msg='Expected club to be returned as a dict')


class CompetitionServicesTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cs = CompetitionService()
        self.cs.competitions = [
            {'name': 'Competition 01',
             'date': '2020-05-01 10:00:00',
             'numberOfPlaces': '20'},
            {'name': 'Competition 02',
             'date': '2020-10-22 15:30:00',
             'numberOfPlaces': '10'}]

    def test_get_competition_by_name_returns_competition_dict(self):
        name = 'Competition 01'
        expected_output = {
            'name': 'Competition 01',
            'date': '2020-05-01 10:00:00',
            'numberOfPlaces': '20'}
        actual_outpout = self.cs.get_competition_by_name(name)
        self.assertEqual(actual_outpout, expected_output,
                         msg='Expected competition to be returned as a dict')


class PurchaseHandlerTest(unittest.TestCase):
    
    def test_init_bad_places_required_raises_value_error(self):
        with self.assertRaises(ValueError,
                               msg='Expected non int value to raise an error'):
            PurchaseHandler('placeholder', 'placeholder', 'dix')


if __name__ == '__main__':
    unittest.main()
