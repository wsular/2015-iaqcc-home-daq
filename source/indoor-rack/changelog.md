Changelog for indoor AQ datalogger
==================================

next version
------------

### Issues Fixed

* Improve error handling for LI-840A

### Data Table Changes

* Rename `li840a_dewpoint` to li840a_dew_T` for internal consistency

### Enhancements

* Restore telemetry reporting (to ScadaBR)


v1.1 [2016-03-12]
-----------------

### Data Table Changes

* Datalogger panel (internal) temperature column renamed from `cr3000_panel_T`
  to `logger_panel_T` in all tables
* Remove CO2 analyzer power source column (`li840a_pwr_src`) from statistics
  table (`stats`)

### Notes

* Increase data retained to internal memory from 7->14 days
* Rename DustTrak II monitoring-only variable from `dusttrak2_pm` to
  `dusttrak2_analog_pm25` and declare private (get via debug table)
* Rename datalogger clock drift from `cr3k_clock_drift` to `clock_drift`


v1.0 [2016-02-24]
-----------------

> After the first round of (summer) measurements, the sampling protocol was
> modified to lower power consumption and limit pump noise. Indoor analyzers
> get consolidated with the outdoor set and redundant devices leave. The
> "outdoor rack" alternates between indoor and outdoor air at 15-min intervals.
> The "indoor rack" still has the Dylos and TSI dust monitors, plus a new
> CO2/H2O analyzer (LI840A; LICOR Biosciences) joins them.

### New instrument line-up

* Alphasense B4-series diffusive gas sensors for CO/NO/O3 (no change)
* Type K thermocouple for ambient air temperature (no change)
* Dylos DC1100 dust monitor (now with wireless DAQ)
* TSI DustTrak II (now monitoring only, using built-in data collection)
* Licor Biosciences LI-840A CO2/H2O analyzer (replacing LGR UGGA for CO2/H2O)

### Known Issues

* Was deployed without Git tag specified so data files will have empty version
  field within station name (first line, second field)

### Issues fixed

* Gas concentration units now correctly specify 'by volume' using a 'v' suffix.
  That is, ppth/ppm/ppb are now ppthv/ppmv/ppbv

### Data Table Changes

* Reduces total days of data retained from 60 to 7
* No data is output to a CompactFlash card -- it all fits within CPU memory.
* Similar to last point, no TOA5-formatted `.dat` files are created (they are
  more difficult to work with and can only be saved to CF card).
* Structure of data tables w.r.t. original indoor air sampling program has
  substantially changed (pre-existing devices do appear in the same order).

### Notes

* DustTrak II signal is monitored and viewable via `debug` data table, but
  values are not recorded -- use TrakPro or a USB flash drive to retrieve the
  data set directly from the device.


v0.6 [2015-08-25]
-----------------

### Data Table Changes

* Write data table files to CompactFlash memory card as cumulative, not daily,
  files. Don't date-stamp files, either. File capacities are 60 days, which is
  much longer than anticipated deployments.
* Change file name formats; where `TABLE` is table name, `YYYYMMDD` is a 
  date-stamp, `X.X` is the program version, and `N` is a sequential value:
  `IAQ15_homeinterior_TABLE_YYYYMMDD.dat` becomes 
  `TOA5_homeinterior(vX.X)_TABLE_N.dat`. The sequential value is automatically
  appended by the datalogger.
* New column tracking 'fit flag' metric from Los Gatos UGGA:
    * `tsdata`: `ugga_fit_flag` after `ugga_self_T`
    * `stats`: `ugga_fit_flag_Avg` after `ugga_self_T_Avg`

### Notes

* Remove daily data file report, both for technical (difficulty of inter-scan
  timing combined with latency of data table generation) and security (high
  susceptibility of email to third-party interception) reasons.
* Increase retry period of daily check-in email from 5- to 15-minutes


v0.5.4 [2015-08-19]
-------------------

### Known Issues

* See note below.

### Issues fixed

* For serial interface devices, ensure averaged values only include data parsed 
  from received records. Prior to fix, first averages include initialization 
  value of 0, which can have dramatic detrimental impact.

    **N.B.** A special condition exists where all values reported via 
    telemetry are 0! This situation is preferrable because of it's 
    apparentness and it arises because the telemetry data table is 
    triggered 1-second before the start of each minute as an inter-scan 
    time-alignment hack. If the logger program begins within 1-minute
    of the next telemetry output interval, the first serial records 
    received will not be included (because they are not checked for
    until 1-second later) and a "NAN" is sent, which ScadaBR interprets 
    as 0. **Final storage data tables are UNAFFECTED.**


v0.5.3 [2015-08-19]
-------------------

### Issues fixed

* Validate parsed messages from Model 205 and Model 405 nm. 
* Re-align telemetry reports to 5-min time base (fixes timestamps trailing
  actual record creation by 1-second)
* Always use midnight as timestamp in data table files (or start-up time, for
  very first file); avoids uncertainty associated with inter-scan triggering by
  simply waiting until a few seconds after midnight to update file names.

### Enhancements

* Send telemetry report of logger clock battery voltage every 6 hours


v0.5.2 [2015-08-19]
-------------------

### Data Table Changes

* Expose all variables (Model 405 nm/NOx, Model 205/O3, UGGA/CH4,CO2)
  in debug table


v0.5.1 [2015-08-18]
-------------------

### Hotfixes

* Rename data table files. Specifically, check for file renaming conditions at
  same frequency as table is called. Fixes regression introduced by 61a9bcfc0b


v0.5 [2015-08-12]
-----------------

### Hotfixes

* Trigger only 1 telemetry report per data table output interval. 96c69a5d19c
  introduced problem causing reports to be sent each second for one minute, 
  per output interval (5min). Fixes #4
* Include data file from diffusive gas sensors in daily report. Has been
  missing because file name is truncated.

### Issues fixed

* Verify Los Gatos UGGA records are correctly parsed by comparing year in data
  record with logger's timestamp (instead of hard-coded "2015"); still relies
  on date/time of both UGGA and datalogger being mostly correct. Latent issue.
* Rename so-called "ambient temperature" measurement from Los Gatos UGGA to
  better reflect actual measurement: `ugga_amb_T` &rarr; `ugga_self_T`; the
  measurement itself has not changed at all but new name is more accurate

### Data table changes

* Data table `tsdata`
    * All columns now represent 1-minute means; affected columns retain their
      original names for consistency though (ie no "_Avg" suffix)
      (affected: `dusttrak2_pm`, `ugga_CH4`, `ugga_H2O`, `ugga_CO2`,
      `ugga_CH4_dry`, `ugga_CO2_dry`, `ugga_gas_P`, `ugga_gas_T`, 
      <del>`ugga_amb_T`</del> `ugga_self_T`, `typeK_amb_T`, `cr3000_panel_T`)
* Data tables `stats` and `telemetry`
    * Are now called frequently enough to perform 1-minute averaging of analog
      and 1Hz signals
    * Have inter-scan locking flags to keep 1-minute data (dylos, m205, m405)
      from being duplicated in averaging calculation
* In all relevant tables, rename the scalar `ugga_amb_T` (& derivatives) to
  `ugga_self_T` (& analagous); refer to *Issues fixed* above
* Fixup debug table to include diffusive gas sensors and regroup (unused) data
  flagging variable with UGGA vars.

### Notes

* Record 1-minute mean values instead of grab samples for TSI DustTrak II,
  Los Gatos Research UGGA, thermocouple and Campbell Scientific CR3000


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

