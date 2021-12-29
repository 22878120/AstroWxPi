#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import board
import math
import adafruit_tsl2591
import adafruit_mlx90614
from adafruit_bme280 import basic as adafruit_bme280

import sys


#Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

# SQM
sqm = adafruit_tsl2591.TSL2591(i2c)

#for an SQM we need the highest gain and longest integration time for maximum sensitivity.
sqm.gain = adafruit_tsl2591.GAIN_LOW
sqm.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS

lSQMCalibFullLuminositySlope = 0.000705244123
lSQMCalibfullLuminosityIntercept = 0.9794303797;
lSQMCalibirSlope = -0.001939421338;
lSQMCalibirIntercept = 1.05;


bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25


#MLX90614 - non-contact infrared thermometer, used to determine the temperature of the sky to 
#detect the presence of clouds. As the sky becomes more clear, the sky temperature 
#is much colder. Comparing the IR temperature with the ambient temperature gives an 
#indication of cloud cover.
mlx = adafruit_mlx90614.MLX90614(i2c)

ln = "\n------------------------------------------------------------"

if __name__ == '__main__':
    while True:
        try:
            now = datetime.datetime.now()
            print(str(now))
                      
            #Get BME280 Temp, Humidity, Pressure, Altitude
            lTemp_c        = bme280.temperature
            lHum           = bme280.relative_humidity
            lPressure_mmHg = bme280.pressure
            lAlt_meters    = bme280.altitude

            print("\nTemperature: %0.1f C" % lTemp_c)  #bme280.temperature)
            print("Humidity: %0.1f %%" % lHum)  #bme280.relative_humidity)
            print("Pressure: %0.1f hPa" % lPressure_mmHg)  #bme280.pressure)
            print("Altitude = %0.2f meters" % lAlt_meters)  #bme280.altitude)

            
            # S Q M
            # Read the total lux, IR, and visible light levels and print it every second.
            # Read and calculate the light level in lux.
            lux = sqm.lux
            print("Total light: {0}lux".format(lux))
            
            lSQM = math.log10(lux/(108000))/-0.4
            print("SQM: {0}".format(lSQM))
            
            
            # You can also read the raw infrared and visible light levels.
            # These are unsigned, the higher the number the more light of that type.
            # There are no units like lux.

            # Infrared levels range from 0-65535 (16-bit)
            ir = sqm.infrared
            #dtaIR=ir
            
            # Visible-only levels range from 0-2147483647 (32-bit)
            visible = sqm.visible
            print("Visible light: {0}".format(visible))
            
            # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
            full_spectrum = sqm.full_spectrum
            
            #Calibrate for temprature
            irCalibrationFactor = lTemp_c * lSQMCalibirSlope + lSQMCalibirIntercept
            fullCalibrationFactor = lTemp_c * lSQMCalibFullLuminositySlope + lSQMCalibfullLuminosityIntercept
            ir = ir * irCalibrationFactor
            full_spectrum = full_spectrum * fullCalibrationFactor
            
            print("Infrared light: {0}".format(ir))
            print("Full spectrum (IR + visible) light: {0}".format(full_spectrum))
            
            #Get MXL90614
            dtaTempAmbient=mlx.ambient_temperature
            dtaTempObject=mlx.object_temperature
            print("\nAmbient Temperature: %0.1f C" % dtaTempAmbient)
            print("IR Temperature: %0.1f C" % dtaTempObject)
            print(ln)
            
            
            
            f = open('/tmp/datafile','w')
            
            f.write('outTemp=')
            f.write(str(round((lTemp_c* 9/5 )+32, 2)))  #save as Fahrenheit 
            f.write('\n')
 
            f.write('outHumidity=')
            f.write(str(round(lHum,2)))
            f.write('\n')
 
            f.write('pressure=')
            f.write(str(round(lPressure_mmHg*0.0295333727,2)))  #save as inHg
            f.write('\n')
 
            f.write('altitude=')
            f.write(str(round(lAlt_meters ,0)))
            f.write('\n')
 
            f.write('total_light_lux=')
            f.write(str(round(lux ,3)))
            f.write('\n')
 
            f.write('sqm=')
            f.write(str(round(lSQM ,2)))
            f.write('\n')
 
            f.write('sky_cover=')
            f.write(str(round(dtaTempObject,2)))
            f.write('\n')
 
 
#            anvil.server.call('store_wx_data',lux,
#                                              lSQM,
#                                              ir,
#                                              visible,
#                                              full_spectrum,
#                                              lTemp,
#                                              lHum,
#                                              lPressure,
#                                              lAlt,
#                                              dtaTempAmbient,
#                                              dtaTempObject)
            f.close
            
        except:
            print("exception")
            print(ln)
        finally:
            time.sleep(60.0)

    app.exec()
