from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np
import pandas as pd
from pandas import DataFrame
import pandas_datareader.data as web

#r = risk-free interest rate
#T = time to maturity
#N = normal cumulative distribution function
#C = call option price
#S = current stock price
#K = strike price
#sigma = volatility of the stock


#Define d1 and d2 from the Black-Scholes formula
def d1(currentPrice, strikePrice, timeToMaturity, interestRate, sigma):
    return(log(currentPrice / strikePrice) + (interestRate + sigma**2 / 2.0) * timeToMaturity) / (sigma * sqrt(timeToMaturity))
def d2(currentPrice, strikePrice, timeToMaturity, interestRate, annualVolatility):
    return d1(currentPrice, strikePrice, timeToMaturity, interestRate, annualVolatility) - annualVolatility * sqrt(timeToMaturity)

#Defines the functions for calls and puts from the Black-Scholes formula
def bs_call(currentPrice, strikePrice, timeToMaturity, interestRate, annualVolatility):
    return currentPrice * norm.cdf(d1(currentPrice, strikePrice, timeToMaturity, interestRate, annualVolatility)) - strikePrice * exp(-interestRate * timeToMaturity) * norm.cdf(d2(currentPrice, strikePrice, timeToMaturity, interestRate, annualVolatility))
def bs_put(currentPrice, strikePrice, timeToMaturity, interestRate, annualVolatility):
    return strikePrice * exp(-interestRate * timeToMaturity) - currentPrice * bs_call(currentPrice, strikePrice, timeToMaturity, interestRate, annualVolatility)

#Defines stock ticker
stockTicker = str(input("Enter stock ticker: "))

#Defines expiry date for option
expiryDate = str(input("Enter expiry date (MM-DD-YYYY): "))

#Defines strike price for option
strikePrice = int(input("Enter strike price: "))

#Defines today as today's date to get accurate data
todayDate = datetime.now()

#Defines the date 1 year ago from today for calculating volatility of stock over the past year
yearPriorDate = todayDate.replace(year=todayDate.year-1)

#Documentation: https://buildmedia.readthedocs.org/media/pdf/pandas-datareader/latest/pandas-datareader.pdf
#Pulls data from Yahoo Finance for the past year for the stock ticker
#web.DataReader(ticker, yahoo, startdate, enddate)
#Gives high, low, open, close, volume, and adjusted close for each day
dataField = web.DataReader(stockTicker, 'yahoo', yearPriorDate, todayDate)

#Sorts data by date
dataField = dataField.sort_values(by="Date")

#Removes rows with missing data
dataField = dataField.dropna()

#Defines priorClose as the data from the day prior to when Close is called for calculating returns
dataField = dataField.assign(priorClose = dataField.Close.shift(1))

#Calculates daily returns for the stock
dataField['returns'] = ((dataField.Close - dataField.priorClose)/dataField.priorClose)

#Calculates the volatility of the stock over the past year
#Volatility is the standard deviation of the returns of the stock over the past year * sqrt(252), # of days market is open
annualVolatility = np.sqrt(252) * dataField['returns'].std()
print(annualVolatility)
#Finds 10-year US Treasury rate from TNX for interest rate
#Uses TNX in Yahoo Finance, prior day's close data, and moves to the correct column (-1), divide by 100 to get decimal form
interestRate = (web.DataReader("^TNX", 'yahoo', todayDate.replace(day = todayDate.day-1), todayDate)['Close'].iloc[-1])/100

#Gets the current price using the last close price
currentPrice = dataField['Close'].iloc[-1]

#Properly formats the expiry date into a datetime object
timeToMaturity = (datetime.strptime(expiryDate, "%m-%d-%Y") - datetime.utcnow()).days / 365

#Outputs the Black-Scholes option price
print("The Option Price is: ", bs_call(currentPrice, strikePrice, timeToMaturity, interestRate, annualVolatility))
