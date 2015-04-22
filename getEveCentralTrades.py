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
import time

db_eveData = 'D:\\EVEData\\eveData.sqlite3'
db_eveSDE = 'D:\\EVEData\\sqlite-scylla.sqlite'
##b_eveSDE = 'D:\\EVEData\\sqlite-latest.sqlite'

runID = int(time.time())

sdeconn = sqlite3.connect(db_eveSDE)
dataconn = sqlite3.connect(db_eveData)

sdeconn.row_factory = sqlite3.Row
dataconn.row_factory = sqlite3.Row

def getIDForName(name, type='system'):

    if type == 'system':
        sql = 'select solarSystemID from mapSolarSystems where solarSystemName = ?'
    if type == 'region':
        sql = 'select regionID from mapRegions where regionName = ?'
    if type == 'market':
        pass
    if type == 'group':
        pass
    if type == 'item':
        pass

    id = ''

    if name:
        for row in sdeconn.execute(sql, (name,)):
            id = row[0]

    return id

def getNameForID(id, type='system'):

    name = ''

    if type == 'system':
        sql = 'select solarSystemName from mapSolarSystems where solarSystemID = ?'
    if type == 'region':
        sql = 'select regionName from mapRegions where regionID = ?'
    if type == 'item':
        sql = 'select typeName from invTypes where typeID = ?'
    if type == 'marketGroup':
        sql = 'select marketGroupName from invMarketGroups where marketGroupID = ?'
    if type == 'group':
        sql = 'select groupName from invGroups where groupID = ?'
    if type == 'category':
        sql = 'select categoryName from invCategories where categoryID = ?'

    if id and sql:
        for row in sdeconn.execute(sql, (id,)):
            name = row[0]

    return name

def getTypeIDInfo(typeID, data=None):

    if data is None:
        data = ( 'marketGroupID', 'groupID', 'categoryID')

    sql = '''select * from invTypes t
                inner join invMarketGroups m on t.marketGroupID = m.marketGroupID
                inner join invGroups g on t.groupID = g.groupID
                inner join invCategories c on g.categoryID = c.categoryID
            where typeID = ?'''
    typeInfo = {}
    for row in sdeconn.execute(sql, (typeID,)):
        for d in data:
            typeInfo[d] = row[d]

    return typeInfo

def getTypeIDs(marketGroup=None, group=None, category=None):
    pass

def storeData(data, table='eveCentralData'):

    dataconn.isolation_level = None

    rows = []
    for d in data:
        cols = data[0].keys()
        tmp = d.values()
        rows.append(list(tmp))

    sql = "insert into {table}( enteredDate, {columns} ) values ( datetime('now'), {bind} )".format(
        table = table, columns = ','.join(cols), bind =','.join('?' for i in range(len(cols)))
    )

    dataconn.executemany(sql, rows)

    print('Total Rows: {0}'.format(dataconn.total_changes))


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
        typeID = item['all']['forQuery']['types'][0]
        info = getTypeIDInfo(typeID)
        tmp = {
            'buyMax': item['buy']['max'],
            'buyMin': item['buy']['min'],
            'buyMedian': item['buy']['median'],
            'buyFivePercent': item['buy']['fivePercent'],
            'buyVolume': item['buy']['volume'],
            'sellMax': item['sell']['max'],
            'sellMin': item['sell']['min'],
            'sellMedian': item['sell']['median'],
            'sellFivePercent': item['sell']['fivePercent'],
            'sellVolume': item['sell']['volume'],
            'typeID': typeID,
            'typeName': getNameForID(typeID, 'item'),
            'systemID': '',
            'systemName': '',
            'regionID': '',
            'regionName': '',
            'marketGroupID': info['marketGroupID'],
            'marketGroupName': getNameForID(info['marketGroupID'], 'marketGroup'),
            'groupID': info['groupID'],
            'groupName': getNameForID(info['groupID'], 'group'),
            'categoryID': info['categoryID'],
            'categoryName': getNameForID(info['categoryID'], 'category'),
            'runID': runID
        }

        if item['all']['forQuery']['systems']:
            tmp['systemID'] = item['all']['forQuery']['systems'][0]
            tmp['systemName'] = getNameForID(item['all']['forQuery']['systems'][0], 'system')
        if item['all']['forQuery']['regions']:
            tmp['regionID'] = item['all']['forQuery']['regions'][0]
            tmp['regionName'] = getNameForID(item['all']['forQuery']['regions'][0], 'region')

        data_store.append(tmp)

    storeData(data_store)

def main():
    TYPEIDS = [ 34,35,36,37,38,39,40,11399,  # Minerals
		19,20,21,22,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,
		11396,17425,17426,17428,17429,17432,17433,17436,17437,17440,17441,
		17444,17445,17448,17449,17452,17453,17455,17456,17459,17460,17463,
		17464,17466,17467,17470,17471,17865,17866,17867,17868,17869,17870,   # ORES
		16273,16272,16275,17887,17888,17889,16274,	# Ice Products
		17975,17976,17977,16262,16269,16268,16267,16266,16265,16264,16263,17978,  # Ice Ores
		3689,44,9832,9848,3683  # PI for fuel blocks
	]

    ## 4 main hubs and the extra for Metro
    SYSTEMIDS = [
        30002187,	## Amarr
        30002659,	## Dodixie
        30000142,	## Jita
        30002510,	## Rens
        30002053,   ## Hek
    ]
    systemnames = ('Amarr', 'Dodixie','Jita', 'Rens', 'Hek')
    regionNames = ( 'Heimatar', 'Metropolis', 'Molden Heath')

    for name in systemnames:
        systemID = getIDForName(name, 'system')
        print("System: %s | %s" % (name, systemID))
        eveCentral(TYPEIDS,system=systemID)
        time.sleep(1)

    for name in regionNames:
        regionID = getIDForName(name, 'region')
        print("Region: %s | %s" % (name, regionID))
        eveCentral(TYPEIDS,system=None,region=regionID)
        time.sleep(1)

##    for systemID in SYSTEMIDS:
##        eveCentral(TYPEIDS, system=systemID)


if __name__ == '__main__':
    main()
