Changelog for outdoor rack
==========================

v1.4.1
------

### Issues Fixed

* Store Licor CO2 analyzer cell pressure data in mbars


v1.4
----

### Known Issues

* Data files headers contain empty version spec because programs were deployed
  without Git tag specified

### Changes to instrument line-up

* Disable CH4/CO2 analyzer (LGR UGGA)

### Data Table Changes

* Add Dylos DC1100 variables to table `debug`

### Issues Fixed

* Harden sample source selection logic (indoor/outdoor valve switching) against
  skipped scans
* Store null values if Dylos DC1100 stops reporting data (instead of holding
  last value)

### Enhancements

* Streamline Licor LI840A integration: sends XML config to sensor, setting it
  to 1Hz reporting of select variables using sparsely formatted strings

### Notes

* Remove ScadaBR integration (query instead via HTTP using Node-RED)
* Re-enables PTR-MS scheduled auto-zero routine
    * Triggered at 02:38, 10:38 and 18:38 (-1h, +8m shift w.r.t. previous)
    * Duration increased 7->15 minutes
    * Schedule is offset so zero routine overlaps half of an indoor period and
      half of an outdoor period
* Remove abandoned code (commented data tables and instrument-specific stuffs)


v1.3
----

### Changes to instrument line-up

* Removed:
    * NO/NO2/NOx (Model 42C; TECO)
    * O3 (Model 205; 2B Technologies)
* Added:
    * NO/NO2/NOx (Model T200U; Teledyne API)
    * O3 (Model T400; Teledyne API)
    * CH4/CO2 (UGGA; Los Gatos Research)

### Data Table Changes

* Remove data tables `stats_indoor` and `stats_outdoor` entirely (since post-
  processing routines consume minutely data)
* Columns renamed:
    * `li840a_dew_T` -> `li840a_dewpoint`
    * `logger_panel_T` -> `logger_self_T`
* Data types reduced from IEEE4 to FP2:
    * `li840a_CO2`, `li840a_H2O`, `li840a_cell_T`,
      `li840a_dewpoint`, `li840a_pwr_src`
* Columns associated with removed instruments have also been removed
* Several new columns associated with added instruments have been added

### Notes

* Disables telemetry reporting to ScadaBR instance
* Disables CO analyzer scheduled auto-zero routine
* Disables PTR-MS scheduled auto-zero routine


v1.2.3
------

### Issues Fixed

* Fix datalogger temperature report (was truncated to single digit width)
* Rehash telemetry reports to reduce overhead:
    * Reconsolidates non-gas data measurements (e.g. ozone is split in/outdoor
      but analyzer cell pressure is not)
    * Construct report URLs as statically as possible
* Send reports *after* sample source flags are updated


v1.2.2 [2016-04-06]
-------------------

### Issues Fixed

* Fix telemetry reports to ScadaBR from outdoor rack (avoid apparent bug with 
  `sprintf()` which causes adjacent string placeholders ("`...%s%s`") to be
  filled with null strings)


v1.2.1 [2016-04-05]
-------------------

### Issues Fixed

* Add DustTrak PM2.5 (analog output) to telemetry reports
* Increase upper range limit of Teledyne CO analyzer from 1.0->10 ppm;
  highest measurement yet has been ~4ppm (data recorded before this fix is 
  truncated, but unaffected data can be collected directly from the analyzer)
* (hidden fix since we always specify device names..) Correctly construct
  reporting URL to ScadaBR if device name is not specified (`""`)
* Force TECO NOx analyzer into correct operating mode by sending relevant
  commands at start-up

### Data Table Changes

* Monitoring table `debug` now exposes all RS232 (string) records from TECO NOx
  box for review

### Enhancements

* Split the telemetry reporting into (3) distinct channel groups:
    * **outdoor-rack** = continuous data from rack (i.e. logger temperature)
    * **outdoor-rack-inside** = gas analyzer data for indoor air sampling
    * **outdoor-rack-outside** = gas analyzer data for outdoor air sampling

### Notes

* Rename `clock_drift` to `NTP_offset` for clarity


v1.2 [2016-04-02]
-----------------

### Changes to instrument line-up

* Add new CO monitor (T300U2; Teledyne API) with just CO being monitored via
  analog output channel #1 (0-1.0 ppmv over 5Vdc)

### Issues Fixed

* Improve error handling for LI-840A
* Reject messages from Model 205 if cell pressure value outside 800-1300 bar
* Fix zero-sampling schedule for CO & PTR-MS and change to these times:
    * 3:30 - 3:37 AM
    * 11:30 - 11:37 AM
    * 7:30 - 7:37 PM

### Data Table Changes

* Add new column `t300_CO` to table `tsdata` before column `m205_O3`
* Rename columns for internal consistency:
    * `m42C_tmpr` -> `m42C_self_T`
    * `li840a_dewpoint` -> li840a_dew_T`
* (hidden change) Change units of LGR UGGA H2O column from parts-per-million to
  parts-per-thousand for consistency with other water vapor columns; won't take
  effect for end-users until device returns from other projects
* Move columns `is_zeroing_PTRMS` and `zflag` to front of file between
  `tflag` and (new column) `t300_CO`

### Enhancements

* Restore telemetry reporting (to ScadaBR)


v1.1 [2016-03-12]
-----------------

### Known Issues

* Auto-zero schedule for PTR-MS was not setup correctly... TODO: figure it out


### Changes to instrument line-up

* Remove LGR CO2/CH4/H2O (UGGA) since it's loaned out to another project (and
  also because we need a control port for PTR-MS zero valve control)
* Remove TECO CO (Model 48) since it's lamp intensity has degraded below 
  minimum required for good measurements

### Issues Fixed

* Rename TECO NOx internal temperature column from `teco_nox` to `m42c_tmpr`
* Add missing units to TECO NOX internal temperature
* Indoor/outdoor separated statistics tables now working properly
* Verify LI-840A serial records parsed correctly by checking cell temperature
  is between 45 and 55 *C (typ. 51 +/- 0.5 *C)

### Data Table Changes

* Datalogger panel (internal) temperature column renamed from `cr3000_panel_T`
  to `logger_panel_T` in all tables
* Remove CO2 analyzer power source column (`li840a_pwr_src`) from statistics
  table (`stats`)
* New columns `is_zeroing_PTRMS` and `zflag`, corresponding to PTR-MS zero
  valve control status
* Reduce precision in stats tables where appropriate (most places):
    `m48_CO`, `m48_CO_zero_Avg`, `m48_cell_T`, `m42C_NO2`, `m42C_NO`, 
    `m42C_NOx`, `m42C_tmpr`, `li840a_cell_T`, `li840a_dewpoint`

### Notes

* Increase data retained to internal memory from 7->14 days
* Rename DustTrak II monitoring-only variable from `dusttrak2_pm` to
  `dusttrak2_analog_pm25` and declare private (get via debug table)
* Rename datalogger clock drift from `cr3k_clock_drift` to `clock_drift`
* Despite removal of CO monitor, update zeroing schedule for CO from 4->3 times
  daily and 5->7 min in duration
* Control/record PTR-MS zero valve, using the same updated schedule as for CO
* Decrease NTP update interval 60->10 min (to match indoor)


v1.0 [2016-02-24]
-----------------

> After the first round of (summer) measurements, the sampling protocol was
> modified to lower power consumption and limit pump noise. Indoor analyzers
> get consolidated with the outdoor set and redundant devices leave. The
> "outdoor rack" alternates between indoor and outdoor air at 15-min intervals.
> The "indoor rack" still has the Dylos and TSI dust monitors, plus a new
> CO2/H2O analyzer (LI840A; LICOR Biosciences) joins them.

### New instrument line-up

* Licor Biosciences LI-840A CO2/H2O analyzer (serial data now, not analog)
* 2B Technologies Model 205 O3 analyzer (supplanting TECO Model 49)
* TECO Model 42C NO/NO2/NOx analyzer (supplanting 2B Tech. Model 405nm)
* TECO Model 48 CO analyzer (now measuring indoor air too)
* Type T thermocouple for gas stream temperature (new)
* TSI DustTrak II (now monitoring only, using built-in data collection)

### Issues fixed

* Gas concentration units now correctly specify 'by volume' using a 'v' suffix.
  That is, ppth/ppm/ppb are now ppthv/ppmv/ppbv
* Remove redundant trailing "(dry)" qualifier from units for `ugga_CH4_dry`
  and `ugga_CO2_dry`

### Data Table Changes

* Reduces total days of data retained from 60 to 7
* No data is output to a CompactFlash card -- it all fits within CPU memory.
* Similar to last point, no TOA5-formatted `.dat` files are created (they are
  more difficult to work with and can only be saved to CF card).
* Structure of data tables w.r.t. original indoor air sampling program has
  substantially changed (pre-existing devices do appear in the same order).

### Notes

* If variable `is_sampling_indoor` is true, the sample air source is from the
  "indoor" side of the 3-way inlet valve (could be through a window, into the
  HVAC return, etc); if false, sample air comes from inverted snorkel inlet
  (typ. on roof top of home).
* The variable `transition_flag` is set high (-1) for the first minute after
  switching sample sources (indoor <--> outdoor).
* DustTrak II signal is monitored and viewable via `debug` data table, but
  values are not recorded -- use TrakPro or a USB flash drive to retrieve the
  data set directly from the device.


outdoor_20150723
----------------

* Revert changes from "outdoor_20150723-test": determined changes did not
  improve data signal quality


outdoor_20150723-test
---------------------

* Remove zero offset applied to LI-840A carbon dioxide signal.


outdoor_20150707
----------------

* Initial field-deployed version, checked in on 2015 July 23 and ostensibly
  unmodified since deployment on 2015 July 7.

