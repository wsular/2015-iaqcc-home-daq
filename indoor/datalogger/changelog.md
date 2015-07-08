Changelog for indoor AQ datalogger
==================================

next version
------------

### Issues fixed

* Add NTP support to keep logger time-synced


v0.1 [2015-07-06]
-----------------

### Known issues

* Data logger time was not updated and NTP code was not included. So logger was
  ~2.5 hours behind until temporary halt in data collection late evening of
  July 10, 2015.
* Does not have the closed-path CO2 analyzer (LI-840A; Licor). It was being
  used elsewhere but the LGR CH4 instrument measures CO2, H2O.

