# HW7 

'''
 Omar Khazamov 

'''

import os
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import numpy as np
import csv
import pandas as pd
import datetime as dt
from dateutil.relativedelta import *
import json
import operator
import copy
import math
import matplotlib.pyplot as plt
import QSTK.qstkstudy.EventProfiler as ep
from dier import Dier
import pdb
import time
import logging
from Mitlib.models import Trade



ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
logging.basicConfig(filename='run.log', level=logging.DEBUG)
# function for sorting csv file from csv how-to

def insertDT(input_list):
    to_be_sorted = copy.deepcopy(input_list)
    for order_piece in to_be_sorted:
        tickDT = dt.date(int(order_piece[0]), int(order_piece[1]), int(order_piece[2]))
        order_piece[0] = tickDT
    return to_be_sorted


class Trader:


    def __init__(self, dataprovider, startdt, enddt, initial_cash):
        self.daily_portfolio_return = []
        self.daily_spy_return = []
        self.dt_start = startdt
        self.dt_end = enddt
        self.cumulativeportval = initial_cash
        self.order_table = []
        self.portfolio = dict
        self.ldt_timestamps = []
        self.tradedates = []
        self.d_data = []
        self.daily_portfolio_val = []
        self.ls_symbols = []


        if dataprovider == 'Yahoo':
                self.dataobj = da.DataAccess('Yahoo')
                self.ldt_timestamps = du.getNYSEdays(self.dt_start, self.dt_end, dt.timedelta(hours=16))
                self.ls_symbols = self.dataobj.get_symbols_from_list('sp5002012')
                self.ls_symbols.append('SPY')
                ldf_data = self.dataobj.get_data(self.ldt_timestamps, self.ls_symbols, ls_keys)
                self.d_data = dict(zip(ls_keys, ldf_data))
        else:
                  self.dataobj = Dier()
        #pdb.set_trace()
                  self.ls_symbols = dataobj.ls_symbols
                  ldf_data = dataobj.get_data()
                  self.d_data = {'close':ldf_data}
                  self.ldt_timestamps = [set(dataobj.ldt_timestamps)]
        Trade.objects.all().delete()

    def output_dates(self):
        return  [datetime.strftime("%d/%m/%y") for datetime in self.ldt_timestamps]

    def process_data(self):
        dt_timeofday = dt.timedelta(hours=16)
        try:
                trade_sorted = Trade.objects.order_by('date')

                portfolio = []
                for row in trade_sorted:
                    portfolio.append(row.ticker)
                    self.tradedates.append(row.date)
                portfolioset = set(portfolio)
                #timestamps for given trade period
                self.ldt_timestamps = du.getNYSEdays(trade_sorted.first().date, trade_sorted.last().date, dt.timedelta(hours=16))



                # ldf_data = self.dataobj.get_data(self.ldt_timestamps, list(portfolioset), ls_keys)
                # #after zipping up with ls_keys, it's basically a dictionary of dictionary
                # self.d_data = dict(zip(ls_keys, ldf_data))
                #need order table to run simulation
                self.order_table = trade_sorted
                #initialize portfolio allocation
                self.portfolio = {x: 0 for x in portfolioset}
                #print self.portfolio

        except Exception, e:
            print e

    def bollinger_bands(self, stock, plot=0):
        dt_start = self.dt_start
        dt_end = self.dt_end

        df_close = self.d_data['close']

        # df_actual_close = self.d_data['actual_close']

        ts_market = df_close['SPY']
        bollinger_band = []
        moving_average = []
        upper_band = []
        lower_band = []
        indicator = np.array([])
        close_price = self.d_data['close'][stock].copy()
        close_price = close_price.fillna(method='ffill')
        close_price = close_price.fillna(method='backfill')
        close_prices = close_price.values

        #for i in range(0, len(self.ldt_timestamps)):

        #price = close_prices[i]
        #if i-20 < 0:
        #roll_idx = 0
        #else:
        #roll_idx = i - 20
        means = pd.stats.moments.rolling_mean(close_prices, 20, min_periods=20)
        stdev = pd.stats.moments.rolling_std(close_prices, 20, min_periods=20)

        upper_band = means + stdev
        lower_band = means - stdev
        bollinger_band = (close_prices - means) / stdev

        if plot:
            plt.clf()
            plt.plot(self.ldt_timestamps, close_prices, label=stock)
            #plt.plot(self.ldt_timestamps, means, label = 'MovAVG')
            #plt.plot(self.ldt_timestamps, upper_band, facecolor   = 'grey', label = None)
            #plt.plot(self.ldt_timestamps, lower_band, facecolor  = 'red', label = None)
            plt.fill_between(self.ldt_timestamps, upper_band.flatten(), lower_band.flatten(), facecolor='grey')
            plt.legend(self.ls_symbols)
            plt.ylabel('Close')
            plt.xlabel('Date')

            # for key, v in zip(self.ldt_timestamps, bollinger_band):
            #     print key, v
        return bollinger_band

    def find_events_wband(self):
        ''' Finding the event dataframe '''
        df_close = self.d_data['close']
        # df_actual_close = self.d_data['actual_close']
        ts_market = copy.deepcopy(df_close['SPY'])
        print "Finding Events"
        # separate out event related parameters
        # from transcation parameters
        #
        number_of_shares = 100
        # Creating an empty dataframe
        df_events = copy.deepcopy(df_close)
        df_events = df_events * np.NAN

        # Time stamps for the event range
        #self.ldt_timestamps = df_close.index
        i = 0
        #print len(self.ldt_timestamps)
        #print len(self.ls_symbols)
        bb_spy_2012 = self.bollinger_bands('SPY')

        for s_sym in self.ls_symbols:
            if s_sym != 'SPY':
                bb = []
                bb = self.bollinger_bands(s_sym)
                for i in xrange(1, len(self.ldt_timestamps)):
                    #print self.ldt_timestamps[i], s_sym

                    # Calculating the returns for this timestamp
                    f_symprice_today = df_close[s_sym].ix[self.ldt_timestamps[i]]
                    f_actual_symprice_today = df_close[s_sym].ix[self.ldt_timestamps[i]]
                    f_symprice_yest = df_close[s_sym].ix[self.ldt_timestamps[i - 1]]
                    f_actual_symprice_yest = df_close[s_sym].ix[self.ldt_timestamps[i - 1]]
                    f_bolband_today = bb[i]
                    f_bolband_yesterday = bb[i - 1]

                    f_marketprice_today = ts_market.ix[self.ldt_timestamps[i]]
                    f_marketprice_yest = ts_market.ix[self.ldt_timestamps[i - 1]]
                    f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
                    f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

                    # Event is found if the symbol is down more then 3% while the
                    # market is up more then 2%
                    #if f_symreturn_today <= -0.03 and f_marketreturn_today >= 0.02:
                    #    df_events[s_sym].ix[ldt_timestamps[i]] = 1

                    #if f_symprice_today < 5 and f_symprice_yest >5:
                    if bb[i] <= -1.0 and bb[i - 1] >= -1.0 and bb_spy_2012[i] >= 1.0:
                        df_events[s_sym].ix[self.ldt_timestamps[i]] = 1

                        buy_year = self.ldt_timestamps[i].year
                        buy_month = self.ldt_timestamps[i].month
                        buy_day = self.ldt_timestamps[i].day
                        idx = i + 5
                        if i + 5 >= len(self.ldt_timestamps):
                            idx = -1
                        sell_year = self.ldt_timestamps[idx].year
                        sell_month = self.ldt_timestamps[idx].month
                        sell_day = self.ldt_timestamps[idx].day

                        buy_date = dt.datetime(buy_year, buy_month, buy_day)
                        sell_date = dt.datetime(sell_year, sell_month, sell_day)

                        Trade.objects.bulk_create([
                            Trade(date=buy_date, ticker=s_sym, operation='BUY', num_shares=number_of_shares),
                            Trade(date=sell_date, ticker=s_sym, operation='SELL', num_shares=number_of_shares)
                        ])




    def find_events(self):
      try:
        #pdb.set_trace()
        ''' Finding the event dataframe '''
        #df_close = self.d_data['close']
        df_actual_close = self.d_data['close']
        ts_market = df_actual_close['SPY']

        print "Finding Events"
        # separate out event related parameters
        # from transcation parameters
        #
        number_of_shares = 100
        # Creating an empty dataframe
        df_events = copy.deepcopy(df_actual_close)
        df_events = df_events * np.NAN

        # Time stamps for the event range
        self.ldt_timestamps = df_actual_close.index
        i = 0

        for s_sym in self.ls_symbols:
            for i in range(1, len(self.ldt_timestamps)):
                # Calculating the returns for this timestamp
                f_symprice_today = df_actual_close[s_sym].ix[self.ldt_timestamps[i]]
                f_actual_symprice_today = df_actual_close[s_sym].ix[self.ldt_timestamps[i]]
                f_symprice_yest = df_actual_close[s_sym].ix[self.ldt_timestamps[i - 1]]
                f_actual_symprice_yest = df_actual_close[s_sym].ix[self.ldt_timestamps[i - 1]]

                f_marketprice_today = ts_market.ix[self.ldt_timestamps[i]]
                f_marketprice_yest = ts_market.ix[self.ldt_timestamps[i - 1]]
                f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
                f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1
                # Event is found if the symbol is down more then 3% while the
                # market is up more then 2%

                if f_actual_symprice_yest >= -2.0 and  f_actual_symprice_today <= -2.0:
                #df_events[s_sym].ix[ldt_timestamps[i]] = 1

                    buy_year = self.ldt_timestamps[i].year
                    buy_month = self.ldt_timestamps[i].month
                    buy_day = self.ldt_timestamps[i].day
                    idx = i + 5
                    if i + 5 >= len(self.ldt_timestamps):
                        idx = -1
                    sell_year = self.ldt_timestamps[idx].year
                    sell_month = self.ldt_timestamps[idx].month
                    sell_day = self.ldt_timestamps[idx].day

                    buy_date = dt.datetime(buy_year, buy_month, buy_day)
                    sell_date = dt.datetime(sell_year, sell_month, sell_day)
                    Trade.objects.bulk_create([
                        Trade(date=buy_date, ticker=s_sym, operation='BUY', num_shares=number_of_shares),
                        Trade(date=sell_date, ticker=s_sym, operation='SELL', num_shares=number_of_shares)
                    ])

      except Exception, E:
          print 'Exception'+E+'occured'

        # ep.eventprofiler(df_events, self.d_data, i_lookback=20, i_lookforward=20,
        # s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
        # s_market_sym='SPY')

        # f.close()

    def jan_trader(self):
        ''' Finding the event dataframe '''
        df_close = self.d_data['close']
        df_actual_close = self.d_data['actual_close']
        ts_market = df_actual_close['SPY']

        #print "Finding Events"
        # separate out event related parameters
        # from transcation parameters
        #
        number_of_shares = 1000
        # Creating an empty dataframe
        df_events = copy.deepcopy(df_actual_close)
        df_events = df_events * np.NAN
        f = open(self.filepath, 'w')
        eventsfile = csv.writer(f, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

        # Time stamps for the event range
        self.ldt_timestamps = df_actual_close.index

        # df_events[s_sym].ix[ldt_timestamps[i]] = 1
        buy_year = "2012"
        buy_month = "12"
        buy_day = "20"
        sell_year = "2013"
        sell_month = "1"
        sell_day = "9"
        enter_trade = [buy_year] + [buy_month] + [buy_day] + ["SPX"] + ['BUY'] + [number_of_shares]
        exit_trade = [sell_year] + [sell_month] + [sell_day] + ["SPX"] + ['SELL'] + [number_of_shares]
        eventsfile.writerows([enter_trade, exit_trade])
        f.close()


    def run(self):
        i = 0
        daily_portfolio_val = []
        # print d_data
        close_prices = self.d_data['close'].copy()
        close_prices = close_prices.fillna(method='ffill')
        close_prices = close_prices.fillna(method='bfill')
        tradedates = []
        #idea is loop through every single day and then, check an order book if the date is in there
        for time in self.ldt_timestamps:
            cash_value = 0
            datestr = str(time).rsplit(' ')[0].rsplit('-')
            datestamp = dt.date(int(datestr[0]), int(datestr[1]), int(datestr[2]))
            samedaytrade = self.tradedates.count(datestamp)
            #handling multiple trades made on the same day
            if samedaytrade != 0:
                for i in range(0, samedaytrade):
                    trade_index = self.tradedates.index(datestamp) + i
                    order = self.order_table[trade_index]
                    if order.operation.upper() == 'BUY':
                        flow = -1
                        self.portfolio[order.ticker] += int(order.num_shares)
                    if order.operation.upper() == 'SELL':
                        flow = 1
                        self.portfolio[order.ticker] -= int(order.num_shares)
                    adj_value = int(order.num_shares) * close_prices[order.ticker][time]
                    #instead of maintaining cash entry in portfolio just use difference between initial cash value and present day portfolio cash value
                    self.cumulativeportval = self.cumulativeportval + adj_value * flow
                    #rebalancing according to daily market fluctuations
                    #important to keep rebalancing outside of the trade orders loop
                    #otherwise daily returns will have multiple entries for the same day and computestats() will return erroneous results

            for ticker in self.portfolio:
                cash_value += self.portfolio[ticker] * close_prices[ticker][time]
            self.daily_portfolio_val.append(self.cumulativeportval + cash_value)
            #print time, self.portfolio, self.cumulativeportval + cash_value

    def computestats(self):

        # nothing fancy, just use library functions to compute daily returns, standard deviation and average of daily returns
        self.daily_portfolio_val /= self.daily_portfolio_val[0]
        self.daily_portfolio_return = tsu.returnize0(self.daily_portfolio_val)
        avg = np.mean(self.daily_portfolio_return)
        stdev = np.std(self.daily_portfolio_return)
        SR = avg / stdev * math.sqrt(252)
        total_return = 1
        for ret in range(1, len(self.daily_portfolio_return)):
            total_return = total_return * (1 + self.daily_portfolio_return[ret])
        #spy_ldf_data = self.dataobj.get_data(self.ldt_timestamps, ['SPY'], ls_keys)
        #d_data = dict(zip(ls_keys, spy_ldf_data))
        close_prices = self.d_data['close'].copy()
        close_prices = close_prices.fillna(method='ffill')
        close_prices = close_prices.fillna(method='bfill')
        na_rets_spy = close_prices['SPY'].values
        self.daily_spy_return = tsu.returnize0(na_rets_spy)




def simulate():

  try:


    logging.info('Log simulate')
    time1 = time.time()
    rstrategy = Trader('Yahoo', dt.datetime(2011, 01, 02), dt.datetime(2012, 12, 06), 100000)

    time2 = time.time()
    logging.info('Class initialization runtime: %f' %(time2-time1))

    rstrategy.find_events_wband()

    time3 = time.time()

    logging.info('find events runtime:  %f' %(time3-time2))

    # rstrategy.jan_trader()

    rstrategy.process_data()

    time4=time.time()
    logging.info('processing data: %f' %(time4-time3))
    rstrategy.run()

    time5=time.time()
    logging.info('run strategy: %f' %(time5-time4))

    rstrategy.computestats()

    time6 = time.time()
    logging.info('compute stats: %f' %(time6-time5))
    #print rstrategy.order_table

  except  AssertionError as AE:
      print "Assertion failed :", format( AE.message)

if __name__ == '__main__':
    simulate()
