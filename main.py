#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Simple demo of the TSL2591 sensor.  Will print the detected light value every second.
import time
import board
import adafruit_tsl2591
from adafruit_bme280 import basic as adafruit_bme280

#Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# Initialize the sensor.
sensor = adafruit_tsl2591.TSL2591(i2c)

# You can optionally change the gain and integration time:
# sensor.gain = adafruit_tsl2591.GAIN_LOW (1x gain)
# sensor.gain = adafruit_tsl2591.GAIN_MED (25x gain, the default)
# sensor.gain = adafruit_tsl2591.GAIN_HIGH (428x gain)
# sensor.gain = adafruit_tsl2591.GAIN_MAX (9876x gain)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS (100ms, default)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS (200ms)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS (300ms)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS (400ms)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS (500ms)
# sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS (600ms)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25


if __name__ == '__main__':
    while True:
        # Read the total lux, IR, and visible light levels and print it every second.
        # Read and calculate the light level in lux.
        lux = sensor.lux
        print("Total light: {0}lux".format(lux))
        # You can also read the raw infrared and visible light levels.
        # These are unsigned, the higher the number the more light of that type.
        # There are no units like lux.

        # Infrared levels range from 0-65535 (16-bit)
        infrared = sensor.infrared
        print("Infrared light: {0}".format(infrared))

        # Visible-only levels range from 0-2147483647 (32-bit)
        visible = sensor.visible
        print("Visible light: {0}".format(visible))

        # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
        full_spectrum = sensor.full_spectrum
        print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))


        #Get BME280
        print("\nTemperature: %0.1f C" % bme280.temperature)
        print("Humidity: %0.1f %%" % bme280.relative_humidity)
        print("Pressure: %0.1f hPa" % bme280.pressure)
        print("Altitude = %0.2f meters" % bme280.altitude)

        time.sleep(1.0)

    app.exec()
