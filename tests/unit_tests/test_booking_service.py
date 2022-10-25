import unittest
from unittest.mock import patch

from services.booking import BookingHandler
from services.club import ClubService
from services.competition import CompetitionService


class BookingHandlerInitTests():

    @patch.object(ClubService, '__init__', return_value=None)
    @patch.object(CompetitionService, '__init__', return_value=None)
    def test_init_ok(self, mock_comp_srv, mock_club_srv):
        bh = BookingHandler('ex club name', 'ex comp name',
                            CompetitionService(), ClubService())
        self.assertEqual(bh.club_name, 'ex club name')
        self.assertEqual(bh.competition_name, 'ex comp name')
        self.assertIsInstance(bh.comp_srv, CompetitionService)
        self.assertIsInstance(bh.club_srv, ClubService)


class BookingHandlerTest(unittest.TestCase):

    @patch.object(ClubService, '__init__', return_value=None)
    @patch.object(CompetitionService, '__init__', return_value=None)
    def setUp(self, mock_comp_srv, mock_club_srv):
        self.bh = BookingHandler('ex club name', 'ex comp name',
                                 CompetitionService(), ClubService())

    @patch("services.club.ClubService.get_club_by_name", return_value='Club01')
    @patch("services.competition.CompetitionService.get_competition_by_name", return_value='Comp01')
    def test_find_booking_data_should_return_dict_with_found_data_if_club_and_competiton_were_found(self, mock_get_comp,  mock_get_club):
        with (patch("services.club.ClubService.was_found", return_value=True)
              and patch("services.competition.CompetitionService.was_found", return_value=True)):
            expected_outcome = {'competition': mock_get_comp.return_value, 'club': mock_get_club.return_value}
            self.assertDictEqual(expected_outcome, self.bh.find_booking_data())

    @patch("services.club.ClubService.get_club_by_name")
    @patch("services.competition.CompetitionService.get_competition_by_name")
    def test_find_booking_data_should_return_None_if_club_and_competiton_were_not_found(self, mock_get_comp, mock_get_club):
        with (patch("services.club.ClubService.was_found", return_value=False)
              and patch("services.competition.CompetitionService.was_found", return_value=False)):
            self.assertIsNone(self.bh.find_booking_data())


if __name__ == '__main__':
    unittest.main()
