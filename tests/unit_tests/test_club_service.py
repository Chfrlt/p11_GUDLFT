import unittest
from unittest.mock import Mock, patch

from services.club import ClubService


class ClubServicesTest(unittest.TestCase):

    def test_was_found_return_true_if_club_passed_is_not_none(self):
        self.assertTrue(ClubService().was_found(club=['placeholder']))

    def test_was_found_return_false_if_club_passed_is_none(self):
        self.assertFalse(ClubService().was_found(club=[]))

    def test_get_club_by_email_return_obj_associated_with_passed_email_if_in_list_of_club(self):
        m1 = Mock(email='ex@em.cf')
        m2 = Mock(email='ab@ng.fr')
        with patch('services.club.repo_get_clubs') as club_list:
            club_list.return_value = [m1, m2]
            expected_return = m1
            self.assertIs(ClubService().get_club_by_email(m1.email), expected_return)
        
    def test_get_club_by_email_return_none_if_passed_email_not_associated_with_club_in_list_of_club(self):
        m1 = Mock(email='ex@em.cf')
        m2 = Mock(email='ab@ng.fr')
        with patch('services.club.repo_get_clubs') as club_list:
            club_list.return_value = [m1, m2]
            self.assertIsNone(ClubService().get_club_by_email('placeholder'))

    def test_get_club_by_name_return_obj_associated_with_passed_name_if_in_list_of_club(self):
        m1 = Mock(club_name='club_ex01')
        m2 = Mock(club_name='ex_club02')
        with patch('services.club.repo_get_clubs') as club_list:
            club_list.return_value = [m1, m2]
            self.assertIs(ClubService().get_club_by_name(m2.club_name), m2)

    def test_get_club_by_name_return_none_if_passed_name_not_associated_with_club_in_list_of_club(self):
        m1 = Mock(club_name='club_ex01')
        m2 = Mock(club_name='ex_club02')
        with patch('services.club.repo_get_clubs') as club_list:
            club_list.return_value = [m1, m2]
            self.assertIsNone(ClubService().get_club_by_name('placeholder'))

    def test_update_clubs_should_return_list_with_updated_club(self):
        mock_list_not_updated = [Mock(club_name='club_ex01'), Mock(club_name='uclub_ex01')]
        mock_update = Mock(club_name='uclub_ex01')
        with patch('services.club.repo_get_clubs', return_value=mock_list_not_updated):
            outcome = ClubService().update_clubs_list(mock_update)
            self.assertIsInstance(outcome, list)
            self.assertIn(mock_update, outcome)

    @patch('services.club.ClubService.get_club_by_email')
    def test_get_club_login_result_should_return_dict(self, mock_get_club):
        expected_keys = ('club', 'msg', 'template')
        # With Club.was_found = True
        with patch('services.club.ClubService.was_found', return_value=True):
            outcome = ClubService().get_club_login_result('placeholder')
            self.assertIsInstance(outcome, dict)
            self.assertIn(next(iter([k for k in outcome])), expected_keys)
        # With Club.was_found = False
        with patch('services.club.ClubService.was_found', return_value=False):
            outcome = ClubService().get_club_login_result('placeholder')
            self.assertIsInstance(outcome, dict)
            self.assertIn(next(iter([k for k in outcome])), expected_keys)

    @patch('services.club.ClubService.get_club_by_email')
    @patch('services.club.ClubService.was_found', return_value=True)
    def test_get_club_login_result_should_return_none_msg_in_dict_if_club_was_found_is_true(self, mock_was_found, mock_get_club):
        returned_msg = ClubService().get_club_login_result('placeholder')['msg']
        self.assertIsNone(returned_msg)

    @patch('services.club.ClubService.get_club_by_email')
    @patch('services.club.ClubService.was_found', return_value=False)
    def test_get_club_login_result_should_return__error_msg_in_dict_if_club_was_found_is_true(self, mock_was_found, mock_get_club):
        expected_msg = "Sorry, that email was not found"
        returned_msg = ClubService().get_club_login_result('placeholder')['msg']
        self.assertEqual(returned_msg, expected_msg)

    @patch('services.club.ClubService.get_club_by_email', return_value='expected_return')
    def test_get_club_login_result_should_return_club_in_dict_(self, mock_get_club):
        # With Club.was_found = True
        with patch('services.club.ClubService.was_found', return_value=True):
            returned_club = ClubService().get_club_login_result('placeholder')['club']
            self.assertEqual(returned_club, mock_get_club.return_value)
        # With Club.was_found = False
        with patch('services.club.ClubService.was_found', return_value=False):
            returned_club = ClubService().get_club_login_result('placeholder')['club']
            self.assertEqual(returned_club, mock_get_club.return_value)

    @patch('services.club.ClubService.get_club_by_email')
    @patch('services.club.ClubService.was_found', return_value=True)
    def test_get_club_login_result_should_return_welcome_template_in_dict_if_club_was_found_is_true(self, mock_was_found, mock_get_club):
        expected = 'welcome.html'
        returned_template = ClubService().get_club_login_result('placeholder')['template']
        self.assertEqual(returned_template, expected)

    @patch('services.club.ClubService.get_club_by_email')
    @patch('services.club.ClubService.was_found', return_value=False)
    def test_get_club_login_result_should_return_index_template_in_dict_if_club_was_found_is_false(self, mock_was_found, mock_get_club):
        expected = 'index.html'
        returned_template = ClubService().get_club_login_result('placeholder')['template']
        self.assertEqual(returned_template, expected)

if __name__ == '__main__':
    unittest.main()
