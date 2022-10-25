import unittest
import json
from unittest.mock import patch

from models.club_model import Club
from models.competition_model import Competition
from services.club import ClubService
from services.competition import CompetitionService
from services.purchase import PurchaseHandler


@patch("repository.competition.filename_comp", new='tests/test.json')
@patch("repository.club.filename_club", new='tests/test.json')
class PurchaseHandlerIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/test.json') as testfile:
            data = json.load(testfile)
            cls.competitions = data['competitions']
            cls.clubs = data['clubs']

    def setUp(self):
        self.competitions = self.__class__.competitions
        self.clubs = self.__class__.clubs
        self.club = Club(self.clubs[0])
        self.comp = Competition(self.competitions[0])
        self.ph = PurchaseHandler(self.club.club_name, self.comp.competition_name,
                                  '2', CompetitionService(), ClubService())

    def test_purchase_places_should_update_club_points(self):
        pre_purchase_club_points = self.club
        club_outcome = self.ph.purchase_places(self.club, self.comp)[0]
        self.assertNotEqual(pre_purchase_club_points, club_outcome.points)

    def test_purchase_places_should_update_competition_places(self):
        pre_purchase_comp_places = self.comp.number_of_places
        comp_outcome = self.ph.purchase_places(self.club, self.comp)[1]
        self.assertNotEqual(pre_purchase_comp_places, comp_outcome.number_of_places)

    def test_execute_purchase_should_return_updated_club_if_purchase_valid(self):
        pre_purchase_club = self.club
        club_outcome = self.ph.execute_purchase()['club'].serialize_club()
        self.assertNotEqual(club_outcome, pre_purchase_club)

    def test_execute_purchase_should_return_updated_comp_list_purchase_valid(self):
        pre_purchase_comps = self.competitions
        comps_outcome = [c.serialize_competition() for c in
                         self.ph.execute_purchase()['competitions']]
        self.assertIsInstance(comps_outcome, list)
        self.assertNotEqual(comps_outcome, pre_purchase_comps)

    def test_is_valid_purchase_should_return_true_if_all_conditions_are_valid(self):
        self.assertTrue(self.ph.is_valid_purchase(self.club, self.comp))

    def test_is_valid_purchase_should_return_false_if_one_or_more_conditions_are_invalid(self):
        # With the club not having enough points:
        with patch('models.club_model.Club.has_enough_points', return_value=False):
            self.assertFalse(self.ph.is_valid_purchase(self.club, self.comp))

    @classmethod
    def tearDownClass(cls):
        with open('tests/test.json', 'w') as testfile:
            dump = json.dumps({'clubs': cls.clubs,
                               'competitions': cls.competitions})
            testfile.write(dump)


if __name__ == '__main__':
    unittest.main()
