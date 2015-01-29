__author__ = 'okhaz'

import xml.etree.ElementTree as ET
import urllib2
import datetime as dt
import numpy
import re
from pandas import TimeSeries
import QSTK.qstkutil.DataAccess as da
import pickle



ls_symbol_len = 5
ls_keys = ['open', 'high', 'low', 'close', 'volume']
#ldf_data_dict1 = numpy.array([])
ldf_data1=[]
ldf_data_dict1 = {}

#HITTING QUOTA WITH MORNINGSTAR FOR THE FULL LIST OF SYMBOLS
ls_symbols = ['GOOG', 'AAPL']


for i in range(0, len(ls_symbols)):
    request = urllib2.Request('https://sandbox.tradier.com/v1/markets/history?symbol='+ls_symbols[i])
    request.add_header('Authorization', 'Bearer ufXQkV1EC3VWP9rnhhCIotuOKMS7')
    f = urllib2.urlopen(request)
    AAPLxml = f.read()


# TODO: replace  by DOM

    eDoc1 = ET.fromstring(AAPLxml)

    j = 0

    ldf_data1_series = TimeSeries()
    assert not isinstance(ldf_data1, numpy.ndarray)
    for day in eDoc1:
    #for i in range(0,len(day)):
    #    print day[i].text

    #ldf_data1.append(day[3].text)
        #TODO: get info on open, high,low and volume as well
        split_list = re.split('-', day[0].text)
        datetime_temp = dt.datetime(int(split_list[0]), int(split_list[1]), int(split_list[2]), 16, 00)
        ldf_data1_series.set_value(datetime_temp, float(day[3].text))




#ldf_resized1 =  numpy.resize(ldf_data1, (j,5))


# need to turn array 90 degrees clock-wise to be able to zip it with symbol keys

#ldf_data_numpy1 = numpy.flipud(numpy.rot90(ldf_resized1))

#for i in range(0,5):
        #TODO: caching
    ldf_data_dict1.update({ls_symbols[i]: ldf_data1_series})





