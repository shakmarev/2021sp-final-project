from datetime import datetime
from functools import reduce
import pandas as pd
from yfinance import Ticker
from luigi import Task, Parameter, LocalTarget


# Obtain and group dividends by year and save it in csv.
class GetDividends(Task):
    ticker = Parameter(default=None)

    def run(self):
        company = Ticker(self.ticker)

        if (company == None):
            return
        # Get dividends using yfinance package.
        dividends = company.dividends.to_frame().reset_index("Date")

        # Since there may be more than one dividends payment within a year I need to group dividends by year.
        divByYear = (
            dividends.groupby(dividends["Date"].dt.year).sum().reset_index("Date")
        )

        # Save results to csv.
        with self.output().open("w") as out_file:
            divByYear.to_csv(out_file, index=False, compression="gzip")

    def output(self):
        return LocalTarget("../data/dividents_ %s.csv" % self.ticker)



# Obtain stock prices and save it in csv.
class GetPrices(Task):
    ticker = Parameter(default=None)

    def run(self):
        company = Ticker(self.ticker)

        if (company == None):
            return
        # Get prices using yfinance package.
        quotes = company.history(period="max")

        # Save results to csv.
        with self.output().open("w") as out_file:
            quotes.to_csv(out_file, index=False, compression="gzip")

    def output(self):
        return LocalTarget("../data/prices_ %s.csv" % self.ticker)


class DDM(Task):
    ticker = Parameter(default=None)
    years = Parameter(default=0)
    rate = Parameter(default=0)
    growth = Parameter(default=0)

    def requires(self):
        return GetDividends(self.ticker)

    def run(self):
        divByYear = pd.read_csv(self.input().open("r")).dropna()["Dividends"]

        #In dividend discount model we do not set observing period, instead we discount and sum all dividends (but future, not past).
        self.years = len(divByYear.index)

        # Discount each dividend
        listOfObservations = list(
            map(
                lambda x, y: (x / (1 + self.rate) ** y),
                divByYear,
                range(1, self.years + 1),
            )
        )
        # Sum all discounted dividends
        sumOfdiv = reduce(lambda x, y: x + y, listOfObservations)

        with self.output().open("w") as out_file:
            out_file.write(
                "{\'observations\': \'%s\', \'terminal\': \'%s\', \'total\': \'%s\'}" % (
                    listOfObservations, 0, sumOfdiv
                )
            )

    def output(self):
        return LocalTarget(
            "../data/value_%s_%s_%s_%s_%s.csv" % (self.ticker, 'DDM', 0, self.rate, self.growth))


class GGM(Task):
    ticker = Parameter(default=None)
    years = Parameter(default=0)
    rate = Parameter(default=0)
    growth = Parameter(default=0)

    def requires(self):
        return GetDividends(self.ticker)

    def run(self):
        divByYear = pd.read_csv(self.input().open("r"))

        # Since analysis is made for N years I only need to get dividends for last N years.
        lastNDiv = divByYear.where(
            divByYear["Date"] > datetime.now().year - self.years
        ).dropna()["Dividends"]

        # Discount each dividend
        listOfObservations = list(
            map(
                lambda x, y: ((((1 + self.growth) / (1 + self.rate)) ** y) * x),
                lastNDiv,
                range(1, self.years + 1),
            )
        )
        # Sum all discounted dividends
        observed = reduce(lambda x, y: x + y, listOfObservations)
        # Obtain value for terminal year
        terminal = listOfObservations[self.years - 1] / (self.rate - self.growth)

        with self.output().open("w") as out_file:
            out_file.write(
                "{\'observations\': \'%s\', \'terminal\': \'%s\', \'total\': \'%s\'}" % (
                    listOfObservations, terminal, observed + terminal
                )
            )

    def output(self):
        return LocalTarget(
            "../data/value_%s_%s_%s_%s_%s.csv" % (self.ticker, 'GGM', self.years, self.rate, self.growth))


def FCF(ticker, years, rate, growth):
    pass


def RI(ticker, years):
    pass


def H(ticker, years, rate, stableYears, stableRate):
    pass


def TWO(ticker, years, rate, stableYears, stableRate):
    pass


def THREE(ticker, years, rate, transitionYears, transitionRate, stableRate):
    pass


class ARIMA(Task):
    ticker = Parameter(default=None)

    def requires(self):
        return GetPrices(self.ticker)

    def run(self):
        prices = pd.read_csv(self.input().open("r")).dropna()["Close"]

        prediction = reduce(lambda x, y: x + y, prices)

        with self.output().open("w") as out_file:
            out_file.write(
                "{\'Price\': \'%s\'}" % (
                    prediction
                )
            )

    def output(self):
        return LocalTarget(
            "../data/prediction_%s.csv" % (self.ticker))
