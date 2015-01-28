__author__ = 'okhaz'

import xml.etree.ElementTree as ET
import urllib2
import pandas as pd

def ls_symbol_len = 5

ls_keys = ['open', 'high', 'low', 'close', 'volume']
ldf_data_dict1 = []

request = urllib2.Request('https://sandbox.tradier.com/v1/markets/history?symbol=GOOG')
request.add_header('Authorization','Bearer ufXQkV1EC3VWP9rnhhCIotuOKMS7')
f = urllib2.urlopen(request)
AAPLxml = f.read()
ldf_data1 = []

#TODO: replace  by DOM

eDoc1 = ET.fromstring(AAPLxml)

j = 0

#an hour of pain for not accounting for j indexing

for day in eDoc1:
        for i in range(0,len(day)):
            #print day[i].text
            assert not isinstance (ldf_data1, numpy.ndarray)

            ldf_data1. append(day[i].text)
            print ldf_data1[i+j-1]
        j += 1


ldf_resized1 = numpy.resize(ldf_data1, (j,5))

# need to turn array 90 degrees clock-wise to be able to zip it with symbol keys

ldf_data_numpy1 = numpy.flipud(numpy.rot90(ldf_resized1))


for i in range(0,5):
    ldf_data_dict1.append({'GOOG':ldf_data_numpy1[i]})


