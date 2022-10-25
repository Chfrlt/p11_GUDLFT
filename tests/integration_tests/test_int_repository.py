import unittest
from unittest.mock import patch, mock_open
import json

from models.club_model import Club
from models.competition_model import Competition
import repository.competition as comp_repo
import repository.club as club_repo


class ClubRepoIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/test.json') as f:
            cls.clubs = json.load(f)['clubs']

    def setUp(self):
        self.clubs = self.__class__.clubs

    @patch("repository.club.filename_club", new='tests/test.json')
    def test_load_clubs_should_return_loaded_clubs_as_club_objects(self):
        outcome = club_repo.load_clubs()
        for club in outcome:
            self.assertIsInstance(club, Club)
            self.assertIn(club.club_name,
                          (c['name'] for c in self.clubs))
            self.assertIn(str(club.points),
                          (c['points'] for c in self.clubs))
            self.assertIn(club.email,
                          (c['email'] for c in self.clubs))


@patch("repository.competition.filename_comp", new='tests/test.json')
class CompetitionRepoIntTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('tests/test.json') as f:
            cls.competitions = json.load(f)['competitions']

    def setUp(self):
        self.comps = self.__class__.competitions

    def test_load_competitions_should_return_list_of_competition_objects(self):
        outcome = comp_repo.load_competitions()
        
        for competition in outcome:
            self.assertIsInstance(competition, Competition)
            self.assertIn(competition.competition_name,
                          (c['name'] for c in self.comps))
            self.assertIn(str(competition.number_of_places),
                          (c['numberOfPlaces'] for c in self.comps))
            self.assertIn(competition.date,
                          (c['date'] for c in self.comps))


if __name__ == '__main__':
    unittest.main()
