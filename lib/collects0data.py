#!/usr/bin/python3

import RPi.GPIO as GPIO
import datetime

pin = sys.argv[1]
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

workfile = '/var/log/gpio-counter-' + str(pin)

counter = 0
while True:
    GPIO.wait_for_edge(pin, GPIO.RISING)
    # reading
    try:
        f = open(workfile, 'ab+')       # open for reading. If it does not exist, create it
        value = int(f.readline().rstrip())  # read the first line; it should be an integer value
    except:
        value = 0               # if something went wrong, reset to 0
    f.close()   # close for reading
    # writing
    f = open(workfile, 'w')
    f.write((str(value+1)+ '\n'))           # the value
    f.write((str(datetime.datetime.now())+ '\n'))   # timestamp
    f.close()

    GPIO.wait_for_edge(pin, GPIO.FALLING)

GPIO.cleanup()