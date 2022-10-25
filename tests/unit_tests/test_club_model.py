import unittest
from random import randint

from models.club_model import Club


class ClubInitTest(unittest.TestCase):
    
    def test_init_ok(self):
        club = Club({'name': 'placeholder', 'points': '10', 'email': 'example@email.com'})
        self.assertEqual(club.club_name, 'placeholder')
        self.assertEqual(club.email, 'example@email.com')
        self.assertEqual(club.points, 10)

    def test_init_bad_points_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            Club({'name': 'Placeholder',
                  'points': 'dix',
                  'email': 'example@email.com'})


class ClubTest(unittest.TestCase):

    def setUp(self) -> None:
        self.club = Club({'name': 'Placeholder',
                          'points': '10',
                          'email': 'example@email.com'})

    def test_is_valid_points_should_return_string_passed_as_int(self):
        actual_outcome = self.club.is_valid_points('10')
        self.assertEqual(actual_outcome, 10)

    def test_is_valid_points_bad_points_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.club.is_valid_points('dix')

    def test_serialize_club_should_return_club_dict(self):
        club = self.club.serialize_club()
        self.assertIsInstance(club, dict)            
        self.assertEqual(club['name'], self.club.club_name)
        self.assertEqual(club['email'], self.club.email)
        self.assertEqual(int(club['points']), self.club.points)

    def test_has_enough_places_should_return_true_if_passed_number_is_inferior_or_equal_to_points(self):
        random_inferior_int = randint(self.club.points - 100,
                                      self.club.points)
        self.assertTrue(self.club.has_enough_points(random_inferior_int))
        self.assertTrue(self.club.has_enough_points(self.club.points))
    
    def test_has_enough_places_should_return_false_if_passed_number_is_superior_to_points(self):
        random_superior_int = randint(self.club.points,
                                      self.club.points + 100)
        self.assertFalse(self.club.has_enough_points(random_superior_int))


if __name__ == '__main__':
    unittest.main()
