from datetime import datetime
from functools import reduce
from csci_utils import io
import pandas as pd
from yfinance import Ticker
from luigi import Task, Parameter, LocalTarget


class GetDividends(Task):
    ticker = Parameter(default=None)

    def run(self):
        company = Ticker(self.ticker)

        if(company == None):
            return

        dividends = company.dividends.to_frame().reset_index("Date")
        divByYear = (
            dividends.groupby(dividends["Date"].dt.year).sum().reset_index("Date")
        )

        with self.output().open("w") as out_file:
            divByYear.to_csv(out_file, index=False, compression="gzip")

    def output(self):
        return LocalTarget("../data/dividents_ %s.csv" % self.ticker)


class GGM(Task):
    ticker = Parameter(default=None)
    years = Parameter(default=0)
    rate = Parameter(default=0)
    growth = Parameter(default=0)

    def requires(self):
        return GetDividends(self.ticker)

    def run(self):
        divByYear = pd.read_csv(self.input().open("r"))

        lastNDiv = divByYear.where(
            divByYear["Date"] > datetime.now().year - self.years
        ).dropna()["Dividends"]

        listOfObservations = list(
            map(
                lambda x, y: ((((1 + self.growth) / (1 + self.rate)) ** y) * x),
                lastNDiv,
                range(1, self.years + 1),
            )
        )
        observed = reduce(lambda x, y: x + y, listOfObservations)
        terminal = listOfObservations[self.years - 1] / (self.rate - self.growth)

        with self.output().open("w") as out_file:
            out_file.write(
                "List of Observations: {0}\nTerminal value: {1}\nTotal value: {2}".format(
                    listOfObservations, terminal, observed + terminal
                )
            )

    def output(self):
        return LocalTarget("../data/price_ %s.txt" % self.ticker)


def FCF(ticker, years, rate):
    pass


def RI(ticker, years):
    pass


def H(ticker, years, rate, stableYears, stableRate):
    pass


def TWO(ticker, years, rate, stableYears, stableRate):
    pass


def THREE(ticker, years, rate, transitionYears, transitionRate, stableRate):
    pass
