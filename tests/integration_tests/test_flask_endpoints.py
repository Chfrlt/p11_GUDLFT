import unittest
import json
import flask_unittest
from unittest.mock import patch, mock_open
from flask.testing import FlaskClient

from app import app


class TestLoginLogout(flask_unittest.AppClientTestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index_should_200(self, _, client: FlaskClient):
        r = client.get('/')
        self.assertStatus(r, 200)
        self.assertInResponse(b'Welcome to the GUDLFT Registration Portal!', r)
        self.assertInResponse(b'Please enter your secretary email to continue', r)

    def test_logout_should_302(self, _, client: FlaskClient):
        r = client.get('/logout')
        self.assertStatus(r, 302)
        self.assertLocationHeader(r, "/")


@patch("repository.competition.filename_comp", new='tests/test.json')
@patch("repository.club.filename_club", new='tests/test.json')
class TestPurchaseFeature(flask_unittest.AppClientTestCase):

    def setUp(self, app, client):
        with open('tests/test.json') as testfile:
            data = json.load(testfile)
            self.competitions = data['competitions']
            self.clubs = data['clubs']
        self.club = self.clubs[0]
        self.comp = self.competitions[0]

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_show_summary_should_render_index_if_email_not_valid(self, _, client: FlaskClient):
        r = client.post('/showSummary', data={'email': 'placeholder'})
        self.assertStatus(r, 200)
        self.assertInResponse(b'Welcome to the GUDLFT Registration Portal!', r)
        self.assertInResponse(b'Please enter your secretary email to continue', r)
        self.assertInResponse(b"Sorry, that email was not found", r)

    def test_show_summary_should_render_welcome_if_email_valid(self, _, client: FlaskClient):
        valid_email = self.club['email']
        r = client.post('/showSummary', data={'email': valid_email})
        self.assertStatus(r, 200)
        self.assertInResponse(f'Welcome, {valid_email}'.encode(), r)
        self.assertInResponse(b'Summary | GUDLFT Registration', r)

    def test_book_should_200_with_valid_club_and_comp_names(self, _, client: FlaskClient):
        club = self.club['name']
        comp = self.comp['name']
        r = client.get('/book/{}/{}'.format(comp, club))
        self.assertStatus(r, 200)
        self.assertInResponse('Booking for {}'.format(comp).encode(), r)

    def test_purchase_places_should_200_if_successfull_purchase(self, _, client: FlaskClient):
        club = self.club
        comp = self.comp
        p_to_purchase = 1
        r = client.post('/purchasePlaces', data={'club': club['name'], 'competition': comp['name'], 'places': p_to_purchase})
        self.assertStatus(r, 200)
        self.assertInResponse(f"Welcome, {club['email']}".encode(), r)
        self.assertInResponse(b'Summary | GUDLFT Registration', r)
        self.assertInResponse('Success-Purchased {} places!'.format(p_to_purchase).encode(), r)

    def test_purchase_places_should_200_if_failed_purchase(self, _, client: FlaskClient):
        club = self.club
        comp = self.comp
        with patch('services.purchase.PurchaseHandler.is_valid_purchase', return_value=False):
            r = client.post('/purchasePlaces', data={'club': club['name'],
                            'competition': comp['name'], 'places': '2'})
            self.assertStatus(r, 200)
            self.assertInResponse(f"Welcome, {club['email']}".encode(), r)
            self.assertInResponse(b'Summary | GUDLFT Registration', r)
            self.assertInResponse(b'Cancelled-Invalid order', r)

    def test_board_should_display_all_clubs(self, _, client: FlaskClient):
        clubs = self.clubs
        r = client.get('/board')
        self.assertStatus(r, 200)
        for club in clubs:
            self.assertInResponse('{}'.format(club['name']).encode(), r)
            self.assertInResponse('{}'.format(club['points']).encode(), r)
            self.assertInResponse('{}'.format(club['email']).encode(), r)

    def tearDown(self, app, client):
        with open('tests/test.json', 'w') as testfile:
            dump = json.dumps({'clubs': self.clubs,
                               'competitions': self.competitions})
            testfile.write(dump)


if __name__ == '__main__':
    unittest.main()
