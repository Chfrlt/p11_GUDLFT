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
    login_result = ClubService().get_club_login_result(request.form['email'])
    competitions = CompetitionService().get_competitions()
    flash(login_result['msg'])
    return render_template(login_result['template'],
                           club=login_result['club'],
                           competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition: str, club: str):
    booking_inst = BookingHandler(club, competition).find_booking_data()
    return render_template('booking.html', club=booking_inst['club'],
                           competition=booking_inst['competition'])


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    purchase_inst = PurchaseHandler(request.form['club'],
                                    request.form['competition'],
                                    request.form['places']).execute_purchase()
    flash(purchase_inst['msg'])
    return render_template('welcome.html',
                           club=purchase_inst['club'],
                           competitions=purchase_inst['competitions'])

@app.route('/board')
def display_board():
    return render_template('board.html', clubs=ClubService().get_clubs())


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
