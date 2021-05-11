
This project provides functionality for analyzing financial data and predicting intrinsic value of securities as well as
predicting price using ARIMA method.

For this purpose I utilize next tools:
yfinance as data provider.
Luigi workflow to download and parse data.
Flask to make user interface.
HTML, CSS and Javascript for visualization.
CanvasJS to ploting graphs.

To start you need to run flask application, then move to Analysis->Fundamentals, insert input values.
Note: Discount rate shuld be greater than growth rate.

For testing purposes you may use next tickers: MSFT, AAPL, F, FF, GM. Unfortunately for some prominent tickers like GOOGL, AMZN, etc. yfinance does not return data. 

For some reason I was not able to run the application on Linux due to Flask-Luigi relted issue "ValueError: signal only works in main thread" https://github.com/d6t/d6tflow/issues/15. On Windows it works fine.