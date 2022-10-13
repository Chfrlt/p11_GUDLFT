from flask import Flask, render_template, request, redirect, flash, url_for

from services.club import ClubService
from services.competition import CompetitionService
from services.purchase import PurchaseHandler
from services.booking import BookingHandler


app = Flask(__name__)
app.secret_key = 'something_special'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    result = ClubService().get_club_by_email(request.form['email'])
    competitions = CompetitionService().get_competitions()
    flash(result['message'])
    return render_template(result['template'], club=result['club'],
                           competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition: str, club: str):
    booking_instance = BookingHandler(club, competition)
    booking_result = booking_instance.find_data()
    flash(booking_result['message'])
    return render_template('booking.html', club=booking_result['club'],
                           competition=booking_result['competition'])


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    purchase_instance = PurchaseHandler(request.form['club'],
                                        request.form['competition'],
                                        request.form['places'])
    purchase_result = purchase_instance.purchase_places()
    flash('Great-booking complete!')
    return render_template('welcome.html',
                           club=purchase_result['club'],
                           competitions=purchase_result['competitions'])


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
