#' PredictPrice
#'
#' This function returns a set of stock prices predicted by ARIMA.
#'
#' @param path path to csv file with stock prices
#' @return A set of predicted prices
#' @export
predictPrice <- function(path){
  prices <- read.csv(path, header=TRUE)
  arimaModel <- arima(tail(prices["Close"], 50), order=c(0,1,2))
  forecast <- predict(arimaModel, 5)
  forecast$pred[1:5]
}
