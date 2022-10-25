from locust import HttpUser, task, between
import logging

from repository.club import get_clubs
from repository.competition import get_competitions


class LocustPerformanceTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def home(self):
        self.client.get('/')

    @task
    def pointsBoard(self):
        self.client.get('/board')

    @task
    def summary(self):
        club = get_clubs()[0]
        self.client.post("/showSummary", data={'email': club.email})

    @task
    def booking_page(self):
        club = get_clubs()[0]
        comp = get_competitions()[0]
        self.client.get(f"/book/{comp.competition_name}/{club.club_name}")

    @task
    def purchasePlaces(self):
        club = get_clubs()[0]
        comp = get_competitions()[0] 
        data = {"competition": comp.competition_name, "club": club.club_name, "places": 1}
        self.client.post('/purchasePlaces', data=data)

    @task
    def logout(self):
        response = self.client.get("/logout")
