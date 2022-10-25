import unittest
import json
from unittest.mock import patch, mock_open

from models.competition_model import Competition
import repository.competition as comp_repo


class CompetitionRepoTest(unittest.TestCase):

    @patch("repository.competition.filename_comp", new='tests/test.json')
    def test_load_competitions_should_return_list(self):
        with patch.object(Competition, '__init__', return_value=None):
            outcome = comp_repo.load_competitions()
            self.assertIsInstance(outcome, list)
            for c in outcome:
                self.assertIsInstance(c, Competition)

    @patch("repository.competition.get_competitions.all_competitions", new=[])
    @patch("repository.competition.load_competitions")
    def test_get_competitions_should_call_load_competitions_if_all_competitions_var_is_empty_list(self, mock_load):
        comp_repo.get_competitions()
        mock_load.assert_called_once()

    @patch("repository.competition.get_competitions.all_competitions", new=[{'foo': 'bar'}])
    @patch("repository.competition.load_competitions")
    def test_get_competitions_should_not_call_load_competitions_if_all_competition_var_is_not_empty_list(self, mock_load):
        comp_repo.get_competitions()
        mock_load.assert_not_called()

    @patch("repository.competition.open")
    @patch("repository.competition.load_competitions", return_value='placeholder')
    def test_get_competitions_should_return_all_competitions_list(self, mock_load, mock_open):
        outpout = comp_repo.get_competitions()
        self.assertIs(outpout, comp_repo.get_competitions.all_competitions)

    @patch("repository.competition.json.dumps", return_value=[{'foo': 'bar'}])
    @patch("repository.competition.load_competitions")
    def test_update_json_should_write_data_in_file(self, mock_load, mock_dumps):
        m = mock_open()
        with patch('repository.competition.open', m, create=True):
            comp_repo.update_competitions_in_json('')
            handle = m()
            handle.write.assert_called_once_with(mock_dumps.return_value)

if __name__ == '__main__':
    unittest.main()
