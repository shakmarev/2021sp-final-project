from flask import Flask, request
from flask import render_template
from luigi import build

from .tasks.tasks import *


app = Flask(__name__)

@app.route('/')
@app.route('/home/')
def index():
    return render_template('index.html')

@app.route('/fundamental/')
@app.route('/fundamental/<ticker>')
def fundamental(ticker=None):
    return render_template('fundamental.html', name=ticker)

@app.route('/fundamental/', methods=['POST'])
def fundamental_post():
    ticker = request.form['ticker'].upper()
    years = request.form['years']
    rate = request.form['rate']
    growth = request.form['growth']
    model = str(request.form['model'])

    switcher = {
        "GGM": build([GGM(ticker=ticker, years=years, rate=rate, growth=growth)], local_scheduler=True),
        "FCF": FCF(ticker, years, rate, growth),
        "RI": RI(ticker, years),
        "H": H(ticker, years, rate, 0, 0),
        "TWO": TWO(ticker, years, rate, 0, 0),
        "THREE": THREE(ticker, years, rate, 0, 0, 0)
    }

    switcher.get(model, lambda: "Invalid model")

    return render_template('fundamental_analysis.html', ticker=ticker)

@app.route('/technical/')
@app.route('/technical/<ticker>')
def technical(ticker=None):
    return render_template('technical.html', name=ticker)

@app.route('/technical/', methods=['POST'])
def technical_post():
    text = request.form['ticker']
    ticker = text.upper()
    return ticker




@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)