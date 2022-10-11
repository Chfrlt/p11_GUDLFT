import unittest

from services.competition import CompetitionService
from services.club import ClubService
from services.purchase import PurchaseHandler


class ClubServicesTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cs = ClubService()
        self.cs.clubs = [
            {'name': 'Club 01',
             'email': 'club01@opclassroom.co',
             'points': '10'},
            {'name': 'Club 02',
             'email': 'club02@opclassroom.com',
             'points': '20'}]

    def test_get_club_by_email_returns_dict(self):
        # should return a dict
        self.assertIsInstance(self.cs.get_club_by_email('placeholder'), dict)
        # when finding a club, it should be returned
        email = 'club01@opclassroom.co'
        expected_output = {
            'name': 'Club 01',
            'email': 'club01@opclassroom.co',
            'points': '10'}
        actual_outpout = self.cs.get_club_by_email(email)
        self.assertEqual(actual_outpout['club'], expected_output,
                         msg='Expected club to be returned as a dict')
        # when club is found, should return None as the ['message'] key
        self.assertEqual(actual_outpout['message'], None,
                         msg='Expected message to be None')
        # when club is found, should return
        # welcome.html as the ['template'] key
        self.assertEqual(actual_outpout['template'], 'welcome.html',
                         msg='Expected template to be "welcome.html"')
        # when club is not found, should return empty list as club
        email = 'wrong@email.co'
        actual_outpout = self.cs.get_club_by_email(email)
        self.assertEqual(actual_outpout['club'], [],
                         msg='Expected club to be an empty list')
        # when club is found, should return
        # "Sorry, that email wasn't found" as the ['message'] key
        self.assertEqual(actual_outpout['message'],
                         "Sorry, that email wasn't found",
                         msg="Expected message to be "
                             "'Sorry, that email wasn't found'")
        # when club is not found, should return
        # index.html as the ['template'] key
        self.assertEqual(actual_outpout['template'], 'index.html',
                         msg='Expected template to be "index.html"')

    def test_login_validation_sould_return_template(self):
        # If club found, should return index.html
        self.assertEqual(self.cs.login_validation(club_found=True),
                         'welcome.html')
        # If club not found, should return index.html
        self.assertEqual(self.cs.login_validation(club_found=False),
                         'index.html')

    def test_was_found_returns_bool(self):
        self.assertIsInstance(self.cs.was_found(club=['placeholder']), bool,
                              msg= 'Expected result to be a bool')
        # If club passed is not None, should return True
        self.assertEqual(self.cs.was_found(club=['placeholder']), True,
                         msg= 'Expected result to be True')
        # If club passed is None, should return False
        self.assertEqual(self.cs.was_found(club=[]), False,
                         msg= 'Expected result to be False')
        

    def test_get_club_by_name_returns_club_dict(self):
        name = 'Club 02'
        expected_output = {
            'name': 'Club 02',
            'email': 'club02@opclassroom.com',
            'points': '20'}
        actual_outpout = self.cs.get_club_by_name(name)
        self.assertEqual(actual_outpout, expected_output,
                         msg='Expected club to be returned as a dict')


class CompetitionServicesTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cs = CompetitionService()
        self.cs.competitions = [
            {'name': 'Competition 01',
             'date': '2020-05-01 10:00:00',
             'numberOfPlaces': '20'},
            {'name': 'Competition 02',
             'date': '2020-10-22 15:30:00',
             'numberOfPlaces': '10'}]

    def test_get_competition_by_name_returns_competition_dict(self):
        name = 'Competition 01'
        expected_output = {
            'name': 'Competition 01',
            'date': '2020-05-01 10:00:00',
            'numberOfPlaces': '20'}
        actual_outpout = self.cs.get_competition_by_name(name)
        self.assertEqual(actual_outpout, expected_output,
                         msg='Expected competition to be returned as a dict')


class PurchaseHandlerTest(unittest.TestCase):

    def test_init_bad_places_required_raises_value_error(self):
        with self.assertRaises(ValueError,
                               msg='Expected non int value to raise an error'):
            PurchaseHandler('placeholder', 'placeholder', 'dix')


if __name__ == '__main__':
    unittest.main()
