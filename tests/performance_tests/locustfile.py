from locust import HttpUser, task, between
import logging

from repository.club import get_clubs
from repository.competition import get_competitions


class LocustPerformanceTest(HttpUser):
    wait_time = between(1, 5)
    def __init__(self, environment):
        self.club = get_clubs()[0]
        self.comp = get_competitions()[0]

    @task
    def home(self):
        self.client.get('/')

    @task
    def pointsBoard(self):
        self.client.get('/board')

    @task
    def summary(self):
        self.client.post("/showSummary", data={'email': self.club.email})

    @task
    def booking_page(self):
        self.client.get(f"/book/{self.competition_name}/{self.club.club_name}")

    @task
    def purchasePlaces(self):        
        data = {"competition": self.comp.competition_name, "club": self.club.club_name, "places": 1}
        self.client.post('/purchasePlaces', data=data)

    @task
    def logout(self):
        response = self.client.get("/logout")

    def tearDown(self):
        with open('tests/test.json', 'w') as testfile:
            dump = json.dumps({'clubs': self.clubs,
                               'competitions': self.competitions})
            testfile.write(dump)
