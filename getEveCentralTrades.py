#-------------------------------------------------------------------------------
# Name:        getEveCentralTrades
# Purpose:
#
# Author:      Gallica
#
# Created:     14/04/2015
# Copyright:   (c) Gallica 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##30002187	Amarr
##30002659	Dodixie
##30000142	Jita
##30002510	Rens

##10000042	Metropolis

import urllib.request
import urllib.parse
import json
import sqlite3

db_data = 'D:\\EVEData\\eveData.sqlite3'

def storeData(dbfile, data):
    conn = sqlite3.connect(dbfile)
    conn.isolation_level = None

    cols = ( 'typeID', 'systemID', 'regionID', 'buyMax', 'buyMin', 'buyMedian',
    'buyFivePercent', 'buyVolume', 'sellMax', 'sellMin', 'sellMedian',
    'sellFivePercent', 'sellVolume')

    sql = 'insert into eveCentralData(enteredDate,'
    sql += ','.join(cols) + ") values (datetime('now'), " + ','.join('?' for i in range(len(cols))) + ')'

    rows = []
    for d in data:
        tmp = []
        for col in cols:
            tmp.append(d[col])
        rows.append(tmp)

    conn.executemany(sql, rows)

    print('Total Rows: {0}'.format(conn.total_changes))
    conn.close()

def eveCentral(typeids, system=30000142, region=None):
    payload = {}
    if region:
        payload['regionlimit'] = region
    else:
        payload['usesystem'] = system

    marketEndpoint = 'http://api.eve-central.com/api/marketstat/json'

    payload['typeid'] = typeids
    data = urllib.parse.urlencode(payload, True)
    data = data.encode('utf-8')

    request = urllib.request.Request(marketEndpoint)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=utf-8')

    response = urllib.request.urlopen(request, data)

    prices = json.loads(response.read().decode('utf-8'))

    data_store = []
    for item in prices:
        tmp = {}
        tmp['buyMax'] = item['buy']['max']
        tmp['buyMin'] = item['buy']['min']
        tmp['buyMedian'] = item['buy']['median']
        tmp['buyFivePercent'] = item['buy']['fivePercent']
        tmp['buyVolume'] = item['buy']['volume']
        tmp['sellMax'] = item['sell']['max']
        tmp['sellMin'] = item['sell']['min']
        tmp['sellMedian'] = item['sell']['median']
        tmp['sellFivePercent'] = item['sell']['fivePercent']
        tmp['sellVolume'] = item['sell']['volume']
        tmp['typeID'] = item['all']['forQuery']['types'][0]

        if system:
            tmp['systemID'] = item['all']['forQuery']['systems'][0]
        else:
            tmp['systemID'] = ''
        if region:
            tmp['regionID'] = item['all']['forQuery']['regions'][0]
        else:
            tmp['regionID'] = ''


        data_store.append(tmp)


    storeData(db_data, data_store)

def main():
    TYPEIDS = [ 34,35,36,37,38,39,40,11399,  # Minerals
		19,20121,22,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,
		11396,17425,17426,17428,17429,17432,17433,17436,17437,17440,17441,
		17444,17445,17448,17449,17452,17453,17455,17456,17459,17460,17463,
		17464,17466,17467,17470,17471,17865,17866,17867,17868,17869,17870,   # ORES
		16273,16272,16275,17887,17888,17889,16274,	# Ice Products
		17975,17976,17977,16262,16269,16268,16267,16266,16265,16264,16263,17978,  # Ice Ores
		3689,44,9832,9848,3683  # PI for fuel blocks
	]

    SYSTEMIDS = [
        30002187,	## Amarr
        30002659,	## Dodixie
        30000142,	## Jita
        30002510,	## Rens
    ]

    for systemID in SYSTEMIDS:
        eveCentral(TYPEIDS, system=systemID)


if __name__ == '__main__':
    main()
