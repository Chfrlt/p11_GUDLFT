import unittest
import json
from unittest.mock import patch, mock_open

from models.club_model import Club
import repository.club as club_repo


class ClubRepoTest(unittest.TestCase):

    @patch("repository.club.filename_club", new='tests/test.json')
    def test_load_clubs_should_return_list_of_club_obj(self):
        with patch.object(Club, '__init__', return_value=None):
            outcome = club_repo.load_clubs()
            self.assertIsInstance(outcome, list)
            for c in outcome:
                self.assertIsInstance(c, Club)

    @patch("repository.club.get_clubs.all_clubs", new=[])
    @patch("repository.club.load_clubs")
    def test_get_clubs_should_call_load_clubs_if_all_club_var_is_empty_list(self, mock_load_clubs):
        club_repo.get_clubs()
        mock_load_clubs.assert_called_once()

    @patch("repository.club.get_clubs.all_clubs", new=[{'foo': 'bar'}])
    @patch("repository.club.load_clubs")
    def test_get_clubs_should_not_call_load_clubs_if_all_club_var_is_not_empty_list(self, mock_load_clubs):
        club_repo.get_clubs()
        mock_load_clubs.assert_not_called()

    @patch("repository.club.get_clubs.all_clubs", new=[{'foo': 'bar'}])
    def test_get_clubs_should_return_all_clubs_list(self):
        outcome = club_repo.get_clubs()
        self.assertEqual(outcome, [{'foo': 'bar'}])

    @patch("repository.club.load_clubs")
    def test_update_json_should_write_data_in_file(self, mock_load_clubs):
        m = mock_open()
        with patch("builtins.open", m, create=True):
            to_write = {'name': 'placeholder',
                        'points': '10',
                        'email': 'ex@plc.np'}
            club_repo.update_clubs_in_json(to_write)
            handle = m()
            handle.write.assert_called_once()


if __name__ == '__main__':
    unittest.main()
