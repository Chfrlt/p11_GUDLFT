import json
import flask_unittest
import unittest
from unittest.mock import patch
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app import app

@unittest.skipIf(__name__ != '__main__', 'Should be run as standalone')
@patch("repository.competition.filename_comp", new='tests/test.json')
@patch("repository.club.filename_club", new='tests/test.json')
class TestValidPurchase(flask_unittest.LiveTestCase):

    @classmethod
    def setUpClass(cls):
        options = ChromeOptions()
        options.add_argument('--headless')
        cls.driver =  Chrome(options=options, service=Service(ChromeDriverManager().install()))
        cls.std_wait = WebDriverWait(cls.driver, 5)
        with open('tests/test.json') as testfile:
            data = json.load(testfile)
            cls.competitions = data['competitions']
            cls.clubs = data['clubs']
            cls.club = cls.clubs[0]

    @classmethod
    def tearDownClass(cls):
        with open('tests/test.json', 'w') as testfile:
            dump = json.dumps({'clubs': cls.clubs,
                               'competitions': cls.competitions})
            testfile.write(dump)
        cls.driver.quit()

    def test_successfull_purchase(self):
        self.driver.get(self.server_url)

        # User login
        login_field = self.std_wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        login_field.send_keys(self.__class__.club['email'])
        login_field.send_keys(Keys.ENTER)
        self.std_wait.until(EC.title_is('Summary | GUDLFT Registration'))

        # User select a competition to book
        self.std_wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Book Places')))
        comp_possible_choices = self.driver.find_elements(By.LINK_TEXT, 'Book Places')
        user_choice = comp_possible_choices[0]
        user_choice.click()
        self.std_wait.until(EC.title_contains('Booking for '))

        # User purchase a set amount of places (default example = 2)
        amount_to_purchase_field = self.std_wait.until(EC.presence_of_element_located((By.NAME, 'places')))
        amount_to_purchase_field.send_keys(2)
        amount_to_purchase_field.send_keys(Keys.ENTER)
        self.std_wait.until(EC.title_is('Summary | GUDLFT Registration'))
        EC.text_to_be_present_in_element((By.TAG_NAME, 'LI'),' Great-booking complete!')

        # User logout
        logout_btn = self.std_wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Logout')))
        logout_btn.click()
        self.std_wait.until(EC.title_is('GUDLFT Registration'))


@unittest.skipIf(__name__ != '__main__', 'Should be run as standalone')
@patch("repository.competition.filename_comp", new='tests/test.json')
@patch("repository.club.filename_club", new='tests/test.json')
class TestInvalidPurchase(flask_unittest.LiveTestCase):

    @classmethod
    def setUpClass(cls):
        options = ChromeOptions()
        options.add_argument('--headless')
        cls.driver =  Chrome(options=options, service=Service(ChromeDriverManager().install()))
        cls.std_wait = WebDriverWait(cls.driver, 5)
        with open('tests/test.json') as testfile:
            data = json.load(testfile)
            cls.competitions = data['competitions']
            cls.clubs = data['clubs']
            cls.club = cls.clubs[0]

    @classmethod
    def tearDownClass(cls):
        with open('tests/test.json', 'w') as testfile:
            dump = json.dumps({'clubs': cls.clubs,
                               'competitions': cls.competitions})
            testfile.write(dump)
        cls.driver.quit()

    def test_unsuccessfull_purchase(self):
        self.driver.get(self.server_url)

        # User login
        login_field = self.std_wait.until(EC.presence_of_element_located((By.NAME, 'email')))
        login_field.send_keys(self.__class__.club['email'])
        login_field.send_keys(Keys.ENTER)
        self.std_wait.until(EC.title_is('Summary | GUDLFT Registration'))

        # User select a competition to book
        self.std_wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Book Places')))
        comp_possible_choices = self.driver.find_elements(By.LINK_TEXT, 'Book Places')
        user_choice = comp_possible_choices[0]
        user_choice.click()
        self.std_wait.until(EC.title_contains('Booking for '))

        # User try to purchase an invalid amount of places (ex = 13)
        amount_to_purchase_field = self.std_wait.until(EC.presence_of_element_located((By.NAME, 'places')))
        amount_to_purchase_field.send_keys(13)
        amount_to_purchase_field.send_keys(Keys.ENTER)
        self.std_wait.until(EC.title_is('Summary | GUDLFT Registration'))
        EC.text_to_be_present_in_element((By.TAG_NAME, 'LI'),'Cancelled-Invalid purchase!')

        # User logout
        logout_btn = self.std_wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Logout')))
        logout_btn.click()
        self.std_wait.until(EC.title_is('GUDLFT Registration'))


def create_app():
    app.config['TESTING'] = True
    app.config['HOST'] = '127.0.0.1'
    app.config['PORT'] = 500
    return app


app = create_app()
suite = flask_unittest.LiveTestSuite(app)
suite.addTest(unittest.makeSuite(TestValidPurchase))
suite.addTest(unittest.makeSuite(TestInvalidPurchase))

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
