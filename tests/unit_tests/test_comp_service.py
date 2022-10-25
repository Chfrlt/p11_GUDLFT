import unittest
from unittest.mock import patch, Mock

from services.competition import CompetitionService

class CompetitionServicesTest(unittest.TestCase):
    
    def test_was_found_should_return_true_if_competition_passed_is_not_none(self):
        self.assertTrue(CompetitionService().was_found(competition=['placehold']),
                         msg= 'Expected result to be False')

    def test_was_found_return_false_if_competition_passed_is_none(self):
        self.assertFalse(CompetitionService().was_found(competition=[]),
                         msg= 'Expected result to be False')

    def test_get_competition_by_name_return_obj_associated_with_passed_name_if_in_list_of_competition(self):
        m1 = Mock(competition_name='comp_ex01')
        m2 = Mock(competition_name='ex_comp02')
        with patch('services.competition.repo_get_competitions') as comp_list:
            comp_list.return_value = [m1, m2]
            self.assertIs(CompetitionService().get_competition_by_name(m2.competition_name), m2)

    def test_get_competition_by_name_return_none_if_passed_name_not_associated_with_competition_in_list_of_competition(self):
        m1 = Mock(competition_name='comp_ex01')
        m2 = Mock(competition_name='ex_comp02')
        with patch('services.competition.repo_get_competitions') as comp_list:
            comp_list.return_value = [m1, m2]
            self.assertIsNone(CompetitionService().get_competition_by_name('placeholder'))

    def test_update_competitions_should_return_list_with_updated_competition(self):
        mock_list_not_updated = [Mock(competition_name='ucomp_ex01'), Mock(competition_name='compe_ex02')]
        mock_update = Mock(competition_name='ucomp_ex01')
        with patch('services.competition.repo_get_competitions', return_value=mock_list_not_updated):
            outcome = CompetitionService().update_competitions_list(mock_update)
            self.assertIsInstance(outcome, list)
            self.assertIn(mock_update, outcome)


if __name__ == '__main__':
    unittest.main()
