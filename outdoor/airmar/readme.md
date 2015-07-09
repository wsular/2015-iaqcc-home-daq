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

Raw data files containing NMEA messages are generated daily and get parsed each
morning into traditional comma-separated values (CSV) files.

### Hardware

The data acquisition system is composed of:

* Laptop (Latitude E6520; Dell) with
    * Windows 7 Enterprise SP1 (Microsoft)
    * [WeatherCaster 3.005 (Airmar)][1]
    * [Python 2.7 (Anaconda 2.2.0 32bit)][2]
    * [GitExtensions 2.48.05][3]
    * [Network Time Protocol 4.2.8p2][4] and
      [NTP Time Server Monitor 1.04][5]
* 200WX weather station ([200WX; Airmar Technology Corp][6]) and
    * 10 meter NMEA 0183 cable (pn 33-862-02)
    * NMEA 0183 to USB Data Converter (pn 33-801-01)
* Lightweight tripod and vertical pole with 3/4" NPT threads

### Physical setup

> TODO

### Software Configuration

#### WeatherCaster

* Copy Start Menu shortcut for WeatherCaster software into user-specific 
  Startup folder so it is launched at login  
  `C:\Users\lar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
* Within the immediate graphical display, verify:
    * `MPS` selected (wind speed)
    * `Celsius` selected (temperatures)
    * `True` selected (wind direction)
    * `mBars` selected (pressure)
    * GMT offset: `-8`
    * Log time: `24`
    * `meters` selected (distances)
* Under Advanced Setup
    * Sensor Hardware
        * Enable/Disable Functionality: under both tabs 'NMEA 0183 Display Settings'
          and 'PC Settings': disable all messages except `GGA`, `MDA` and set
          intervals to `0:10.00`.
    * Communications/Diagnostics
        * Set raw data log path to `C:\Users\lar\Desktop\200WX raw data`
    * Names
        * Verify Storage identify is set to 'Use Sensor Serial Numbers'


#### Windows 7

* Ensure computer remains in the Pacific Standard Time zone year-round:
    * Open Date & Time settings
    * Click 'Change time zone'
    * Verify selection is "(UTC -08:00) Pacific Time (US & Canada)"
    * Deselect checkbox 'Automatically adjust clock for Daylight Saving Time'
    * Press 'OK' twice
* Install copy of Airmar 200WX processing script, if not present:

````
C:\Users\lar> cd Desktop
C:\Users\lar\Desktop> git clone https://bitbucket.org/wsular/2015-iaq-intensive-daq.git
````

* Schedule the Airmar file processing script to run daily:
    * Launch Task Scheduler and choose Create Task...
    * Provide name "Process Airmar 200WX files" under 'General' tab
    * Switch to 'Triggers' and choose New...
        * Change schedule to Daily, starting "today", at 6:00:00 AM
        * Enable 'Stop task if runs longer than: ' and set to '4 hours'
    * Switch to 'Actions' and choose New...
        * Provide path to python script as 'Program/script'  
        `C:\Users\lar\Desktop\2015-iaq-intensive-daq\outdoor\airmar\juice_airmar_files.py`
        * Add directory arguments  
        `"C:\Users\lar\Desktop\200WX raw data" -d "C:\Users\lar\Desktop\200WX csv format"`
* Other changes
    * Stop & disable the Windows Update service
    * [Enable automatic login of "lar" user account at boot][7]


#### Network Time Protocol

* Installation of `ntp-4.2.8p2-win32-setup.exe`:
    * DO create configuration file and select for public NTP servers
      North America -> United States of America
    * DO create new account for service;
      name:`local_ntpd`, password: `BoringPassword4BoringNTP`
* Installation of `ntp-time-server-monitor-104.exe`:
    * No special instructions for install
    * After completed, open Properties of the created Start Menu shortcut,
      switch to Compatibility tab and select 'Run this program as an
      administator'. Press OK.
* Configuration of NTP Time Server Monitor
    * Switch to 'Statistic' tab; click 'Yes' to enable statistics and restart
      the service. *This will not work if NTP Server Monitor is not run as an
      administrator.*


  [1]: http://www.airmartechnology.com/2009/about/download-software.php
  [2]: http://continuum.io/downloads
  [3]: http://sourceforge.net/projects/gitextensions/
  [4]: https://www.meinbergglobal.com/english/sw/ntp.htm#ntp_stable
  [5]: https://www.meinbergglobal.com/english/sw/ntp-server-monitor.htm
  [6]: http://www.airmartechnology.com/2009/products/marine-product.asp?prodid=200
  [7]: http://www.sevenforums.com/tutorials/377-log-automatically-startup.html
