import argparse
from luigi import build
from final.tasks.tasks import *


parser = argparse.ArgumentParser(description="Process analysis.")
parser.add_argument("-t", "--ticker", default="AAPL")
parser.add_argument("-y", "--years", default=5)
parser.add_argument("-d", "--data", default="dividends")
args = parser.parse_args()

def main(args=None):
    build([GGM(ticker="AAPL", years=5, rate=0.1, growth=0.05)], local_scheduler=True)

if __name__ == "__main__":
    main(args)