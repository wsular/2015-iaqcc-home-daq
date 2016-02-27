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

