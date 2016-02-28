Changelog for outdoor AQ DAQFactory program
===========================================

next version
------------

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

