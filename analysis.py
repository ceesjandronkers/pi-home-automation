import influxdb
import pandas
import datetime as dt
import matplotlib.pyplot as plt

def getdataset(values, spaces, timefilter):
    # Set up a client for InfluxDB
    dbclient = influxdb.DataFrameClient('192.168.1.70', 8086, 'root', 'root', 'sensordata')

    # get data
    if timefilter != "": timefilter = " AND " + timefilter
    data = pandas.DataFrame()
    for value in values:
        for space in spaces:
            rs = dbclient.query('SELECT mean(value) FROM "' + value + '" WHERE "ruimte" = \'' + space + '\'' + timefilter + ' GROUP BY time(5m), "ruimte" fill(linear)')
            datacol = list(rs.values())[0]
            datacol.columns = [space +'-'+value]
            if data.empty:
                data = datacol
            else:
                data = data.join(datacol,how='outer')
    dbclient.close()
    return data


test = getdataset(['temperatuur'],["gastenkamer", "buiten2"],"time < now() and time > now() - 2d")
test['gastenkamer-temperatuur-avg'] = pandas.Series(test['gastenkamer-temperatuur'].rolling(12,center=True).mean(), index=test.index)
test['buiten2-temperatuur-avg'] = pandas.Series(test['buiten2-temperatuur'].rolling(12,center=True).mean(), index=test.index)
test['gastenkamer-temperatuur-delta'] = test['gastenkamer-temperatuur-avg'] - test['buiten2-temperatuur-avg']
test['gastenkamer-temperatuur-roc'] = test['gastenkamer-temperatuur-avg'].diff()
test['gastenkamer-temperatuur-rocperdegree'] = test['gastenkamer-temperatuur-roc'] / test['gastenkamer-temperatuur-delta']*12
test['gastenkamer-temperatuur-rocperdegree'] = test['gastenkamer-temperatuur-rocperdegree'].rolling(12,center=True).mean()
#test[['gastenkamer-temperatuur-avg','buiten2-temperatuur','gastenkamer-temperatuur-rocperdegree','gastenkamer-temperatuur-roc']].plot()
test[['gastenkamer-temperatuur-rocperdegree']].plot()
plt.ylim(-0.1,0.4)
plt.show()