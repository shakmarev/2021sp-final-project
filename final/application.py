import os

from flask import Flask, request, render_template
from luigi import build

from final.tasks.tasks import *


app = Flask(__name__)

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/fundamental/')
@app.route('/fundamental/<ticker>')
def fundamental(ticker=None):
    return render_template('fundamental.html', name=ticker)

@app.route('/fundamental/', methods=['POST'])
def fundamental_post():
    ticker = request.form['ticker'].upper()
    years = int(request.form['years'])
    rate = float(request.form['rate'])
    growth = float(request.form['growth'])
    model = str(request.form['model'])

    #Custom switch-case implementation
    switcher = {
        "GGM": build([GGM(ticker=ticker, years=years, rate=rate, growth=growth)], local_scheduler=True),
        "FCF": FCF(ticker, years, rate, growth),
        "RI": RI(ticker, years),
        "H": H(ticker, years, rate, 0, 0),
        "TWO": TWO(ticker, years, rate, 0, 0),
        "THREE": THREE(ticker, years, rate, 0, 0, 0)
    }

    switcher.get(model, lambda: "Invalid model")

    #Load data obtained by Luigi tasks.
    path = os.path.abspath("../data/price_%s_%s_%s_%s.txt" % (ticker, years, rate, growth))
    f = open(path, "r")
    result = eval(f.read())

    #Create data to visualize discounted dividends by year
    lastYear = datetime.now().year
    firstYear = lastYear - years+1
    listOfYears = range(firstYear, lastYear+1)
    observations = eval(result['observations'])
    points = list(map(lambda y, o: {'label': y, 'y': o}, listOfYears, observations))

    #Pass variables to flask template
    content = {'model': model,
               'ticker': ticker,
               'years': years,
               'rate': rate,
               'growth': growth,
               'observations': observations,
               'terminal': result['terminal'],
               'total': result['total'],
               'points': points
		}

    return render_template('fundamental_analysis.html', **content)

@app.route('/technical/')
@app.route('/technical/<ticker>')
def technical(ticker=None):
    return render_template('technical.html', name=ticker)

@app.route('/technical/', methods=['POST'])
def technical_post():
    text = request.form['ticker']
    ticker = text.upper()
    return ticker

if __name__ == '__main__':
    app.run(debug=True)
