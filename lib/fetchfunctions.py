from urllib.request import urlopen
import json
try:
    import Adafruit_DHT
except ImportError:
    # Mockup class for windows testing
    class Adafruit_DHT:
        DHT22 = 0
        def read_retry(a, b):
            return (50, 10)
import sqlite3
import subprocess

def getsolardata(devicenaam):
    data = subprocess.run("/usr/local/bin/sbfspot.3/SBFspot -v", shell=True) #-finq (toevoegen als hij weer te vroeg stopt))
    c = sqlite3.connect("/home/openhabian/SMA/smadata/SBFspot.db").cursor()
    c.execute("select case when strftime('%s',datetime('now')) - Timestamp < 240 THEN 'Ja' ELSE 'Nee' END As Actueel, EToday, TotalPac from Inverters;")
    results = c.fetchone()
    if(results[0]=='Ja'):
        data = {devicenaam + "/EToday": results[1], devicenaam + "/TotalPAc": results[0]}
    else:
        data = {}
    c.close()
    return data


def gettemperaturesensordata(poort, ruimtenaam):
    data = dict()
    # Try to grab a sensor reading.  Use the read_retry method which will retry up
    # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
    data[ruimtenaam + "/luchtvochtigheid"], data[ruimtenaam + "/temperatuur"] = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,poort)
    return data


def getweatherdata(url, object, mapping):
    data = dict()
    # Load data
    meteo = urlopen(url).read()
    meteo = meteo.decode('utf-8')
    weather = json.loads(meteo)

    # Fetch data based on mapping
    for key, value in mapping.items():
        datavalue = weather[object][key]
        if isinstance(datavalue,str):
            datavalue = float(datavalue.replace('%',''))
        data[value["channel"]] = datavalue * value["factor"] + value["offset"]

    return data

def gets0data(devicenaam, pin)
    data = dict()
    f = open(workfile, 'ab+')  # open for reading. If it does not exist, create it
    data[devicenaam + "/Whstand"] = float(f.readline().rstrip())  # read the first line; it should be an integer value
    f.close()  # close for reading
    # writing
    # f = open(workfile, 'w')
    # f.write((str(0) + '\n'))  # the value
    # f.write((str(datetime.datetime.now()) + '\n'))  # timestamp
    # f.close()
    return data
