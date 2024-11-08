################################################################
# CSCI 6502 - Jahoon Koo, Jhansi Saketa
# stocks.py
# This file uses Yahoo Finance API to receive Apple stock quotes
# 
################################################################

import time
import yfinance as yf

data = yf.download(tickers='AAPL', period='1d', interval='1h')
# filter out unnecessary columns from stock quotes 
l1=list(data[len(data)-2:len(data)-1][0:])
l=[0,0]
l[0]=l1[:len(l1)-1]
lp=data[len(data)-2:len(data)-1][0:].values
l[1]=lp.tolist()[0][:len(lp.tolist()[0])-1]

