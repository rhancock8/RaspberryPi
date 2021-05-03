#!/usr/bin/env python3

import time
import colorsys
import sys, getopt
try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except:
    import ltr559

from bme280 import BME280
from pms5003 import PMS5003, ReadTimeoutError as pmsReadTimeoutError
from enviroplus import gas
from subprocess import PIPE, Popen
import logging


# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# PMS5003 particulate sensor
try:
    pms5003 = PMS5003()
except:
    logging.warning("Failed to initialise PMS5003")

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

# The main routine
def main(argv):
    valuename = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["valuename="])
    except getopt.GetoptError:
        print("poll_enviro.py --valuename=<valuename to poll>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("poll_enviro.py --valuename=<valuename to poll>")
            print("where valuename can be ONE of the following:")
            print("temp , pressure , humidity , lux , air-oxidised , air-reduced , air-nh3 , air-pm1 , air-pm10 , air-pm25")
            sys.exit()
        elif opt in ("-v", "--valuename"):
           valuename = arg

    if valuename == '':
        print("poll_enviro.py --valuename=<valuename to poll>")
        sys.exit(2)

    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("""poll_enviro.py - output enviro %s sensor value\n""",valuename)

    # Tuning factor for compensation. Decrease this number to adjust the
    # temperature down, and increase to adjust up
    factor = 2.25

    cpu_temps = [get_cpu_temperature()] * 5

    delay = 0.5  # Debounce the proximity tap
    mode = 0     # The starting mode
    last_page = 0
    light = 1

    # One mode for each variable
    if valuename == "temp":
        # variable = "temperature"
        unit = "C"
        cpu_temp = get_cpu_temperature()
        # Smooth out with some averaging to decrease jitter
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        try:
            raw_temp = bme280.get_temperature()
            data = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
        except:
            logging.warning("Failed to read PMS5003")
            data = -1
        print(data)

    if valuename == "pressure":
        # variable = "pressure"
        unit = "hPa"
        try:
            data = bme280.get_pressure()
        except:
            logging.warning("Failed to read BME280")
            data = -1
        print(data)

    if valuename == "humidity":
        # variable = "humidity"
        unit = "%"
        try:
            data = bme280.get_humidity()
        except:
            logging.warning("Failed to read BME280")
            data = -1
        print(data)

    if valuename == "lux":
        proximity = -1
        try:
            proximity = ltr559.get_proximity()
        except:
            logging.warning("Failed to read LTR559 (proximity)")

        # variable = "light"
        unit = "Lux"
        if proximity < 10:
            try:
                data = ltr559.get_lux()
                logging.warning("Failed to read LTR559 (light-level)")
            except:
                data = -1
        else:
            data = 1
        print(data)

    if valuename == "air-oxdised":
        # variable = "oxidised"
        unit = "kO"
        data = gas.read_all()
        data = data.oxidising / 1000
        print(data)

    if valuename == "air-reduced":
        # variable = "reduced"
        unit = "kO"
        data = gas.read_all()
        data = data.reducing / 1000
        print(data)

    if valuename == "air-nh3":
        # variable = "nh3"
        unit = "kO"
        data = gas.read_all()
        data = data.nh3 / 1000
        print(data)

    if valuename == "air-pm1":
        # variable = "pm1"
        unit = "ug/m3"
        try:
            data = pms5003.read()
        except pmsReadTimeoutError:
            logging.warning("Failed to read PMS5003")
            data = -1
        else:
            data = float(data.pm_ug_per_m3(1.0))
        print(data)

    if valuename == "air-pm25":
        # variable = "pm25"
        unit = "ug/m3"
        try:
            data = pms5003.read()
        except pmsReadTimeoutError:
            logging.warning("Failed to read PMS5003")
            data = -1
        else:
            data = float(data.pm_ug_per_m3(2.5))
        print(data)

    if valuename == "air-pm10":
        # variable = "pm10"
        unit = "ug/m3"
        try:
            data = pms5003.read()
        except pmsReadTimeoutError:
            logging.warning("Failed to read PMS5003")
            data = -1
        else:
            data = float(data.pm_ug_per_m3(10))
        print(data)

    sys.exit(0)

if __name__ == "__main__":
   main(sys.argv[1:])

