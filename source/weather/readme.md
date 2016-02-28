Weather station
===============

Indoor Air Quality (2015)
-------------------------

A compact, ultrasonic weather station is deployed outside the home to capture
basic meteorological conditions:

* Horizontal wind speed (meters/second) and direction (degrees East of North)
* Ambient temperature (degrees Celcius)
* Dew point temperature (degrees Celcius)
* Relative humidity (percent)
* Barometric pressure (millibars)

The actual data acqusition is out-sourced in this repository (which is private
while in development, but should be open by the time you read this):

    <https://bitbucket.org/patricktokeeffe/rpi-airmar-200wx/>

### Parts

* 200WX weather station ([200WX; Airmar Technology Corp][url-airmar]) and
    * 10 meter NMEA 0183 cable (pn 33-862-02)
    * NMEA 0183 to USB Data Converter (pn 33-801-01)
* Lightweight tripod and vertical pole with 3/4" NPT threads
* Single-board Linux computer ([Raspberry Pi B+]-based data acquisition, with
    * long (75') weather-resistant Ethernet cable
    * passive power-over-ethernet injector/extractor set

  [url-airmar]: http://www.airmartechnology.com/2009/products/marine-product.asp?prodid=200
  [url-rpi]: http://raspberrypi.org


### Physical setup

> TODO



