import os

from flask import Flask, request, render_template
from luigi import build

from final.tasks.tasks import *


app = Flask(__name__)

@app.route('/')
@app.route('/home/')
@app.route('/index/')
def index():
    """ A simple index page """
    return render_template('index.html')

@app.route('/about/')
def about():
    """ Information about the project """
    return render_template('about.html')

@app.route('/fundamental/')
def fundamental(ticker=None):
    """ Show fundamental analysis page"""
    return render_template('fundamental.html', name=ticker)

@app.route('/fundamental/', methods=['POST'])
def fundamental_post():
    """ Perform fundamental analysis"""
    ticker = request.form['ticker'].upper()
    model = str(request.form['model'])
    years = int(request.form['years']) if model != "DDM" else 0
    rate = float(request.form['rate'])
    growth = float(request.form['growth'])

    #Custom switch-case implementation
    switcher = {
        "DDM": build([DDM(ticker=ticker, rate=rate, growth=growth)], local_scheduler=True),
        "GGM": build([GGM(ticker=ticker, years=years, rate=rate, growth=growth)], local_scheduler=True),
        "FCF": FCF(ticker, years, rate, growth),
        "RI": RI(ticker, years),
        "H": H(ticker, years, rate, 0, 0),
        "TWO": TWO(ticker, years, rate, 0, 0),
        "THREE": THREE(ticker, years, rate, 0, 0, 0)
    }

    switcher.get(model, lambda: "Invalid model")

    #Load data obtained by Luigi tasks.
    path = os.path.abspath("../data/value_%s_%s_%s_%s_%s.csv" % (ticker, model, years, rate, growth))
    f = open(path, "r")
    result = eval(f.read())

    #Create data to visualize discounted dividends
    observations = eval(result['observations'])
    lastYear = datetime.now().year
    firstYear = lastYear - years + 1 if model != "DDM" else len(observations) + 1
    listOfYears = range(firstYear, lastYear+1)
    points = list(map(lambda y, o: {'label': y, 'y': o}, listOfYears, observations))

    #Pass variables to flask template
    content = {'model': model,
               'ticker': ticker,
               'years': years if model != "DDM" else len(observations),
               'rate': rate,
               'growth': growth,
               'observations': observations,
               'terminal': result['terminal'],
               'total': result['total'],
               'points': points
		}

    return render_template('fundamental_analysis.html', **content)

@app.route('/technical/')
def technical(ticker=None):
    """Show technical analysis page"""
    return render_template('technical.html', name=ticker)

@app.route('/technical/', methods=['POST'])
def technical_post():
    """Perform technical analysis"""
    ticker = request.form['ticker'].upper()
    build([ARIMA(ticker=ticker)], local_scheduler=True)

    #Load data obtained by Luigi tasks.
    path = os.path.abspath("../data/prediction_%s.csv" % (ticker))
    f = open(path, "r")
    result = f.read()

    #Pass variables to flask template.
    content =  {'ticker': ticker,
                'total': result
                }
    return render_template('technical_analysis.html', **content)

if __name__ == '__main__':
    app.run(debug=False)
