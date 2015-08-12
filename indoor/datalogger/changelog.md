Changelog for indoor AQ datalogger
==================================

next version
------------

### Hotfixes

* Trigger only 1 telemetry report per data table output interval. 96c69a5d19c
  introduced problem causing reports to be sent each second for one minute, 
  per output interval (5min). Fixes #4
* Include data file from diffusive gas sensors in daily report. Has been
  missing because file name is truncated.


v0.4 [2015-08-10]
-----------------

### Issues fixed

* Set methane analyer (UGGA) values to NAN if no new record is received (BB #3)
* Don't truncate UGGA sample cell pressure values in telemetry reports
* Expose clock drift variable in debug table

### Data table changes

* New columns added to end of tables, in order listed here:
    * Tables `tsdata` and `debug`: `typeK_amb_T`, `cr3000_panel_T`
    * Tables `stats` and `telemetry`: `typeK_amb_T_Avg`, `cr3000_panel_T_Avg`
* New data table `B4_sensors` containing
    * Carbon monoxide, millivolts and ppb (`B4_CO_mV`, `B4_CO_est`)
    * Nitric oxide, millivolts and ppb (`B4_NO_mV`, `B4_NO_est`)
    * Ozone, millivolts and ppb (`B4_O3_mV`, `B4_O3_est`)
    * Columns are grouped by units (mV, then ppb), listed in alphabetical order

### Enhancements

* Add routine to send test email; accessible via panel menu, Public table
* Measuring ambient temperature using thermocouple (at gas sampling inlet)
* Perform exploratory measurements of carbon monoxide (CO), nitric oxide (NO),
  and ozone (O3) using electrochemical sensors (B4-series; Alphasense)
    * Reported in both measured (mV) and engineering units (ppb)
    * Scaling determined by linear regression of multi-point cal. assessment
    * Data stored in separate table file, included with daily report

### Notes

* Routines using network services are relocated from primary scan to a slow
  sequence (affected: test ScadaBR report) so measurements cannot be impacted
  by timeouts
* Data table `debug` is updated at 1Hz when active (half as frequent)
* Telemetry reports now include derived value `dc1100_size_ratio`, which
  is natural logarithm of ratio of small to large particle counts (or NAN if
  large counts is 0)


v0.3 [2015-07-23]
-----------------

### Issues fixed

* Keep point 0 (first) at midnight (00:00:00) in data files. 
  [#2](https://bitbucket.org/wsular/2015-iaq-intensive-daq/issues/2/)

### Data table changes

* All columns prefixed with "gga30p_" are updated to prefix "ugga_"; this is
  the manufacturer's common name as evidenced by advertising. 
* Table files are now date-stamped before final storage or email reporting;
  the time is included and will not be midnight only on the day the logger
  program started running
* Column `m205_O3_lo_fi` is removed from both tables `tsdata` and `stats`)

### Notes

* No longer recording analog voltage signal from 2B Technologies Model 205 
  ozone monitor (`m205_O3_lo_fi`); the serial data stream is determined to be
  sufficiently reliable now


v0.2.2 [2015-07-11]
-------------------

### Hotfixes

* Still observe symptoms even with large buffers so clear buffers after each
  record is read
* Also, move telemetry stuffs into email slowsequence; missing records are 
  observed to correlate with the period following whole 5-min intervals and
  the telemetry table is both processed on 5-minutes and requires network
  comms, which is susceptible to timeouts, etc


v0.2.1 [2015-07-11]
-------------------

### Hotfixes

* Observe symptoms of #1 occur after skipped record in table `tsdata` (1min);
  increase the incoming record buffer sizes for O3, NOx monitors
* Include Git tag in start-up email
* Remove duplicate call to debug table


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

