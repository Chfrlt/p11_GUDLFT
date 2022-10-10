import json
from flask import Flask, render_template, request, redirect, flash, url_for

from services.club import ClubService


def load_competitions():
    with open('competitions.json') as comps:
        competitions_list = json.load(comps)['competitions']
        return competitions_list


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = ClubService().get_club_by_email(request.form['email'])
    return render_template('welcome.html', club=club,
                           competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = ClubService().get_club_by_name(club)
    found_competition = (
        [c for c in competitions if c['name'] ==
         competition][0]
        )
    if found_club and found_competition:
        return render_template('booking.html', club=found_club,
                               competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = (
        [c for c in competitions if c['name'] ==
         request.form['competition']][0]
        )
    club = ClubService().get_club_by_name(request.form['club'])
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = (
        int(competition['numberOfPlaces']) - places_required
        )
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
