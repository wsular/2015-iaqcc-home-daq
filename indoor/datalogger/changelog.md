Changelog for indoor AQ datalogger
==================================

next version
------------

### Hotfixes

* Observe symptoms of #1 occur after skipped record in table `tsdata` (1min);
  increase the incoming record buffer sizes for O3, NOx monitors
* Include Git tag in start-up email


v0.2 [2015-07-10]
-----------------

### Issues fixed

* Add NTP support to keep logger time-synced
* Incidentally resolve 
  [issue #1](https://bitbucket.org/wsular/2015-iaq-intensive-daq/issues/1/) by
  re-integrating the ozone monitor's analog voltage signal (Model 205; 2B Tech)
* Datalogger attempts to send daily email up to (3) times

### Data table changes

* String representing station name now contains the Git tag in parentheses so
  relevant program version is tracked in data files, not repo tag names plus
  spreadsheet.
* New column `m205_O3_lo_fi` in table `tsdata` between columns `dc1100_pm_large`
  and `m205_O3`
* New column `m205_O3_lo_fi_Avg` in table `stats` between columns
  `dc1100_pm_large_Avg` and `m205_O3_Avg`

### Notes

* Now also recording analog voltage signal from ozone monitor
* Datalogger's 'Station Name' is modified each deployment because it contains
  the release's Git tag.


v0.1 [2015-07-06]
-----------------

### Known issues

* Data logger time was not updated and NTP code was not included. So logger was
  ~2.5 hours behind until temporary halt in data collection late evening of
  July 10, 2015.
* Does not have the closed-path CO2 analyzer (LI-840A; Licor). It was being
  used elsewhere but the LGR CH4 instrument measures CO2, H2O.

