import json
from flask import Flask, render_template, request, redirect, flash, url_for

from services.club import ClubService
from services.competition import CompetitionService


app = Flask(__name__)
app.secret_key = 'something_special'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = ClubService().get_club_by_email(request.form['email'])
    competitions=CompetitionService().competitions
    return render_template('welcome.html', club=club,
                           competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = ClubService().get_club_by_name(club)
    found_competition = CompetitionService().get_competition_by_name(competition)
    if found_club and found_competition:
        return render_template('booking.html', club=found_club,
                               competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=CompetitionService().competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = CompetitionService().get_competition_by_name(competition)
    club = ClubService().get_club_by_name(request.form['club'])
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = (
        int(competition['numberOfPlaces']) - places_required
        )
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club,
                           competitions=CompetitionService().competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
