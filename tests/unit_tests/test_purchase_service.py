import unittest
from unittest.mock import patch
from random import randint

from services.purchase import PurchaseHandler
from services.club import ClubService
from services.competition import CompetitionService
from models.club_model import Club
from models.competition_model import Competition


class PurchaseHandlerTest(unittest.TestCase):

    @patch.object(ClubService, '__init__', return_value=None)
    @patch.object(CompetitionService, '__init__', return_value=None)
    def setUp(self, mock_comp_srv, mock_club_srv) -> None:
        self.ph = PurchaseHandler('placeholder', 'placeholder', '10',
                                  CompetitionService(), ClubService())

    @patch.object(ClubService, '__init__', return_value=None)
    @patch.object(CompetitionService, '__init__', return_value=None)
    def test_init_ok(self, mock_comp_srv, mock_club_srv):
        club_srv_inst = ClubService()
        comp_srv_inst = CompetitionService()
        ph_inst = PurchaseHandler('ex_club_name', 'ex_comp_name', '10',
                                comp_srv_inst, club_srv_inst)
        self.assertEqual(ph_inst.club_name, 'ex_club_name')
        self.assertEqual(ph_inst.competition_name, 'ex_comp_name')
        self.assertEqual(ph_inst.places_required, 10)
        self.assertIs(ph_inst.comp_srv, comp_srv_inst)
        self.assertIs(ph_inst.club_srv, club_srv_inst)

    @patch.object(ClubService, '__init__', return_value=None)
    @patch.object(CompetitionService, '__init__', return_value=None)
    def test_init_bad_places_required_raises_value_error(self, mock_comp_srv, mock_club_srv):
        with self.assertRaises(ValueError):
            PurchaseHandler('placeholder', 'placeholder', 'dix',
                            CompetitionService(), ClubService())

    def test_is_places_required_should_return_string_passed_as_int(self):
        self.assertEqual(self.ph.is_valid_places_required('10'), 10)
    
    def test_is_places_required_bad_places_required_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            self.ph.is_valid_places_required('dix')

    def test_places_required_is_no_more_than_12_should_return_true_if_places_required_is_inferior_than_12(self) -> bool:
        with patch.object(self.ph, 'places_required', new=randint(-100, 11)):
            self.assertTrue(self.ph.places_required_is_no_more_than_12())

    def test_places_required_is_no_more_than_12_should_return_true_if_places_required_is_equal_to_12(self) -> bool:
        with patch.object(self.ph, 'places_required', 12):
            self.assertTrue(self.ph.places_required_is_no_more_than_12())

    def test_places_required_is_no_more_than_12_should_return_false_if_places_required_is_superior_than_12(self) -> bool:
        with patch.object(self.ph, 'places_required', randint(13, 100)):
            self.assertFalse(self.ph.places_required_is_no_more_than_12())

    @patch('services.club.ClubService.get_club_by_name')
    @patch('services.competition.CompetitionService.get_competition_by_name')
    @patch('services.club.ClubService.update_clubs_json')
    @patch('services.competition.CompetitionService.update_competitions_json')
    def test_execute_purchase_should_return_dict(self, mock_update_comp, mock_update_club,
                                                 mock_get_comp, mock_get_club):
        expected_keys = ('competitions', 'club', 'msg')
        # With is_valid_purchase = True
        with patch('services.purchase.PurchaseHandler.is_valid_purchase', return_value=True):
            outcome = self.ph.execute_purchase()
            self.assertIsInstance(outcome, dict)
            for k in outcome:
                self.assertIn(k, expected_keys)
        # With is_valid_purchase = False
        with patch('services.purchase.PurchaseHandler.is_valid_purchase', return_value=False):
            outcome = self.ph.execute_purchase()
            self.assertIsInstance(outcome, dict)
            for k in outcome:
                self.assertIn(k, expected_keys)

    @patch('services.club.ClubService.get_club_by_name')
    @patch('services.competition.CompetitionService.get_competition_by_name')
    def test_execute_purchase_should_return_error_message_in_dict_if_purchase_not_valid(self, mock_get_comp, mock_get_club):
        with patch('services.purchase.PurchaseHandler.is_valid_purchase', return_value=False):
            expected_msg = 'Cancelled-Invalid order'
            returned_msg = self.ph.execute_purchase()['msg']
            self.assertEqual(returned_msg, expected_msg)

    @patch('services.club.ClubService.get_club_by_name')
    @patch('services.club.ClubService.update_clubs_json')
    @patch('services.competition.CompetitionService.get_competition_by_name')
    @patch('services.competition.CompetitionService.update_competitions_json')
    def test_execute_purchase_should_return_confirmation_message_in_dict_if_purchase_is_valid(self, mock_comp_update,
                                                                                              mock_get_comp, mock_club_update, mock_get_club):
        with patch('services.purchase.PurchaseHandler.is_valid_purchase', return_value=True):
            expected_msg = f'Success-Purchased {self.ph.places_required} places!'
            returned_msg = self.ph.execute_purchase()['msg']
            self.assertEqual(returned_msg, expected_msg)

    @patch('services.club.ClubService.get_club_by_name')
    @patch('services.club.ClubService.update_clubs_json')
    @patch('services.competition.CompetitionService.get_competition_by_name')
    @patch('services.competition.CompetitionService.update_competitions_json')
    @patch('services.purchase.PurchaseHandler.execute_purchase')
    def test_execute_purchase_should_purchase_places_if_purchase_is_valid(self, mock_exe, mock_comp_update,
                                                                          mock_get_comp, mock_club_update, mock_get_club):
        with patch('services.purchase.PurchaseHandler.is_valid_purchase', return_value=True):
            self.ph.execute_purchase()
            mock_exe.assert_called_once()


if __name__ == '__main__':
    unittest.main()
