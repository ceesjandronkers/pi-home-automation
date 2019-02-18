#!/usr/bin/python3
import time
import paho.mqtt.client as mqtt
import lib.fetchfunctions as fetchfunctions

def main():
    data = dict()

    # Fetch data
    data.update(fetchfunctions.gettemperaturesensordata(17,"gastenkamer"))
    data.update(fetchfunctions.gettemperaturesensordata(17, "temp"))
    #data.update(fetchfunctions.gets0data(23, "warmtepomp"))
    #data.update(fetchfunctions.gets0data(24, "boilerelement"))
    mappingWU = {"temp_c": {"channel": "buiten/temperatuur", "factor":1, "offset":0},
                "solarradiation": {"channel": "buiten/instraling", "factor":1, "offset":0},
               "wind_degrees": {"channel": "buiten/windrichting", "factor":1, "offset":0},
               "wind_gust_kph": {"channel": "buiten/windsnelheid", "factor":1, "offset":0},
               "relative_humidity": {"channel": "buiten/luchtvochtigheid", "factor":1, "offset":0}
               }
    data.update(fetchfunctions.getweatherdata("http://api.wunderground.com/api/41c27b6d8fbe37d7/conditions/q/NL/Mijdrecht.json",'current_observation',mappingWU))
    mappingDarkSky = {"temperature": {"channel":"buiten2/temperatuur", "factor":1/1.8, "offset":-32/1.8},
               "cloudCover": {"channel":"buiten2/bewolking", "factor":1, "offset":0},
               "windBearing": {"channel":"buiten2/windrichting", "factor":1, "offset":0},
               "windSpeed": {"channel":"buiten2/windsnelheid", "factor":1, "offset":0},
               "humidity": {"channel":"buiten2/luchtvochtigheid", "factor":100, "offset":0}
               }
    data.update(fetchfunctions.getweatherdata("https://api.darksky.net/forecast/f9fa7a9d42c56df81c448305dbd2b3af/52.2084,4.8143",'currently',mappingDarkSky))
    #data.update(fetchfunctions.getsolardata("zonnepanelen"))

    daikindataset = {
        'keuken/temperatuur': '{"m2m:rqp":{"op":2,"to":"/[0]/MNAE/1/Sensor/IndoorTemperature/la","fr":"/S",rqi":"ywduj"}}',
        'tuin/temperatuur': '{"m2m:rqp":{"op":2,"to":"/[0]/MNAE/1/Sensor/OutdoorTemperature/la","fr":"/S","rqi":"ywduj"}}',
        'warmtepomp/DHWtemperatuur': '{"m2m:rqp":{"op":2,"to":"/[0]/MNAE/2/Sensor/TankTemperature/la","fr":"/S","rqi":"sfobl"}}',
        }
    data.update(fetchfunctions.getdaikindata(daikindataset))

    # Write values to MQTT
    mqttc = mqtt.Client()
    mqttc.connect("localhost", 1883, 60)
    for key, value in data.items():
        if value is not None:
            mqttc.publish(key, value)
            # without a delay, the client disconnects for some reason
            time.sleep(0.1)
    mqttc.disconnect()

if __name__ == "__main__":
    main()