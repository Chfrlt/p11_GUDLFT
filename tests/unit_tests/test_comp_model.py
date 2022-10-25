import datetime
import unittest
from random import randint
from unittest.mock import patch

from models.competition_model import Competition


class CompetitionInitTest(unittest.TestCase):
    
    def test_init_ok(self):
        competition = Competition(
            {'name': 'Placeholder',
             'date': '2020-03-27 10:00:00',
             'numberOfPlaces': '10'})
        self.assertEqual(competition.competition_name, 'Placeholder')
        self.assertEqual(competition.date, '2020-03-27 10:00:00')
        self.assertEqual(competition.number_of_places, 10)

    def test_init_bad_number_of_places_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            Competition(
                {'name': 'Placeholder',
                 'date': '2020-03-27 10:00:00',
                 'numberOfPlaces': 'dix'})


class CompetitionServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.competition = Competition(
            {'name': 'Placeholder',
             'date': '2000-03-27 10:00:00',
             'numberOfPlaces': '10'})

    def test_is_valid_number_of_places_should_return_str_as_int(self):
        actual_outcome = self.competition.is_valid_number_of_places('10')
        self.assertEqual(actual_outcome, 10)

    def test_is_valid_number_of_places_bad_number_of_places_should_raise_error(self):
        with self.assertRaises(ValueError):
            self.competition.is_valid_number_of_places('dix')

    def test_serialize_competition_should_return_dict(self):
        competition = self.competition.serialize_competition()
        self.assertIsInstance(competition, dict)
        self.assertEqual(competition['name'],
                         self.competition.competition_name)
        self.assertEqual(competition['date'], self.competition.date)
        self.assertEqual(int(competition['numberOfPlaces']),
                         self.competition.number_of_places)

    @patch('models.competition_model.datetime')
    def test_date_has_not_passed_should_return_fasle_if_anterior_date(self, mock_dtime):
        mock_dtime.datetime.now.return_value = datetime.datetime(2000, 1, 15, 9, 30, 00)
        mock_dtime.datetime.strptime.return_value = datetime.datetime(1800, 1, 15, 9, 30, 00)
        self.assertFalse(self.competition.date_has_not_passed())

    @patch('models.competition_model.datetime')
    def test_date_has_not_passed_should_return_true_if_ulterior_date(self, mock_dtime):
        mock_dtime.datetime.now.return_value = datetime.datetime(2000, 1, 15, 9, 30, 00)
        mock_dtime.datetime.strptime.return_value = datetime.datetime(3000, 1, 15, 9, 30, 00)
        self.assertTrue(self.competition.date_has_not_passed())

    def test_has_enough_places_should_return_true_if_passed_number_is_inferior_to_nbr_of_places(self):
        random_inferior_int = randint(self.competition.number_of_places - 100,
                                      self.competition.number_of_places)
        self.assertTrue(self.competition.has_enough_places(random_inferior_int))

    def test_has_enough_places_should_return_true_if_passed_number_is_equal_to_nbr_of_places(self):
        self.assertTrue(self.competition.has_enough_places(self.competition.number_of_places))

    def test_has_enough_places_should_return_false_if_passed_number_is_superior_to_nbr_of_places(self):
        random_superior_int = randint(self.competition.number_of_places,
                                      self.competition.number_of_places + 100)
        self.assertFalse(self.competition.has_enough_places(random_superior_int))


if __name__ == '__main__':
    unittest.main()
