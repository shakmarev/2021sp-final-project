.. 2021sp-final-project-shakmarev documentation master file, created by
   sphinx-quickstart on Mon May 10 19:24:01 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to 2021sp-final-project-shakmarev's documentation!
==========================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Documentation
=============
Intro
-----

This project provides functionality for analyzing financial data and predicting intrinsic value of securities as well as
predicting price using ARIMA method.

Overview
--------
My project can be roughly divided into three parts: data collection and preparation, calculations and analysis, and presenting outcomes.
I utilize Luigi workflow to download and parse data.

The input data come from Yahoo Finance through yfinance package and saved in csv files.
Analysis is made in Python as well as in R, and R code called from python using rpy2 package.
Resulting values are visualized on html page thanks to CanvasJS library as well as printed of exported to PDF.

To start you need to run flask application, then move to Analysis->Fundamental (or Technical), insert input values.
For testing purposes you may use next tickers: MSFT, AAPL, F, FF, GM. Unfortunately for some prominent tickers like GOOGL, AMZN, etc. yfinance does not return data.
For some reason I was not able to run the application on Linux due to Flask-Luigi relted issue "ValueError: signal only works in main thread" https://github.com/d6t/d6tflow/issues/15. On Windows it works fine.

Architecture
------------
1. User opens any address.
2. Application.py routs user to the corresponding html page.
3. If user posts some data which are requered for calculation, then router calls luigi tasks.
4. Fundamental analysis tasks get data from Yahoo Finance using yfinance package. After calculation resulting values returned to router and published on html page.
5. Html page generates visual diagram using CanvasJS.
6. Technical analysis task gets data from the same package and saves it to csv file. Then saved data processed further to R function which is called through rpy2 package.
7. Resulting data published on html page.

Diagram of the architecture
+++++++++++++++++++++++++++
.. image:: /images/architecture.png
   :align:   center

Code
----
Here is how I use flask to render simple html template::

   @app.route('/technical/')
   def technical(ticker=None):
       return render_template('technical.html', name=ticker)


And this is an example how to call luigi task from flask::

   @app.route('/technical/', methods=['POST'])
   def technical_post():
       ticker = request.form['ticker'].upper()
       build([ARIMA(ticker=ticker)], local_scheduler=True)


Example of calling R code from python::

   def predictPrices(path):
       r = robjects.r
       sourcepath = os.path.abspath("rpy2/project/R/predict.R")
       source = r.source(sourcepath)
       from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage
       project = SignatureTranslatedAnonymousPackage("predictPrice <- " + str(source[0]), "project")
       return project.predictPrice(path)


Example of R code::

   predictPrice <- function(path){
     prices <- read.csv(path, header=TRUE)
     arimaModel <- arima(tail(prices["Close"], 50), order=c(0,1,2))
     forecast <- predict(arimaModel, 5)
     forecast$pred[1:5]
   }

Autodoc
-------
final.tasks.tasks module
++++++++++++++++++++++++

.. automodule:: final.tasks.tasks
   :members:
   :undoc-members:
   :show-inheritance:


final.application module
++++++++++++++++++++++++

.. automodule:: final.application
   :members:
   :undoc-members:
   :show-inheritance:


Conclusion
----------
In my project I've tried to combine R functionality with Python functionality using rpy2 package.

The system can be improved. Some ideas:

* Make a good readable reports.
* Add functionality for estimating cost of not only stocks, but also other financial instruments such as bonds and options.
* Use other analytical methods to predict cost, such as neural networks, linear regression, regression trees and so on.
* Add more visualizations.
* Add an API so other systems can use it.


