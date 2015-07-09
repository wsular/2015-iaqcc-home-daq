# -*- coding: utf-8 -*-
"""
Airmar data file juicer

Searches a directory for data files made by Airmar weather station and
re-writes files into comma-separated format containing:

* ISO8601-compliant timestamp
* Barometric pressure, mbar
* Ambient temperature, degC
* Relative humidity, %
* Dew point temperature, degC
* Wind direction, degEofTN and degEofMN
* Wind speed, m/s

The search directory is provided as first command line argument; if not
specified, it defaults to the working directory. Similarly, the output
directory can be provided as the second command line argument and, if missing,
will default to the working directory.

"""

import os, os.path as osp
import argparse

from datetime import datetime
from glob import glob

opts = argparse.ArgumentParser()
opts.add_argument("source",
                  help="Full path to directory containing input files")
opts.add_argument("-d", "--dest",
                  help="Full path to output directory; default: working directory")
args = opts.parse_args()
if not args.dest:
    args.dest = os.getcwd()


#list of relevant measurements recorded
columns = ['"Date and Time",'
          '"Barometric Pressure",'
          '"Air Temperature",'
          '"Relative Humidity",'
          '"Dew Point",'
          '"Wind Direction (True N)",'
          '"Wind Direction (Magnetic N)",'
          '"Wind Speed"']

#list of units for recorded measurements
column_units = ['"YYYY-MM-DD hh:mm:ss.sss(GMT -8)",'
                '"milibars",'
                '"degC",'
                '"percent",'
                '"degC",'
                '"degTrue",'
                '"degMag",'
                '"m/s"']

header = ",".join(columns) + "\n"
units = ",".join(column_units) + '\n'


def squeeze_met_data(airmar_filepath, date):
    """Extract meterological data from raw 200WX data file"""
    fpath, fname = osp.split(airmar_filepath)
    oname = osp.splitext(fname)[0] + '.dat'

    print "Extracting data from", fname
    try:
        os.makedirs(args.dest)
    except OSError:
        if not osp.isdir(args.dest):
            raise

    with open(osp.join(args.dest, oname), mode='w') as outfile:
       with open(airmar_filepath, mode='r') as datafile:
            outfile.write(header)
            outfile.write(units)
            for line in datafile:
                #each data protocol key is divided by a $ identifier
                time, data = line.split('$')
                timestamp = date.strftime('"%Y-%m-%d ' + time[:-5] + '"' )
                #WIMDA is data protocol key for the meteorological composite
                if data.startswith('WIMDA'):
                    (key, bpi, bpiu, bp, bpbu, at, atu, wt, wtu,
                     rh, ah, dp, dpu, wdt, wdtu, wdm, wdmu, wsk,
                     wsku, wsm, wsmu) = data.split(',')
                #returns 'NAN' if no measurement was recorded
                    #converts barometric pressure (bars) to mbars
                    if bp:
                        bp = "{:.1f}".format( float(bp)*1000 )
                    else:
                        bp = '"NAN"'
                    if not at: at = '"NAN"'
                    if not rh: rh = '"NAN"'
                    if not dp: dp = '"NAN"'
                    if not wdt: wdt = '"NAN"'
                    if not wdm: wdm = '"NAN"'
                    if not wsm: wsm = '"NAN"'
                    dataout = (timestamp +
                            "," + bp + "," + at + "," + rh +
                            "," + dp + "," + wdt + "," + wdm +
                            "," + wsm +'\n')
                    outfile.write(dataout)


rawfiles = glob(osp.join(args.source, '*.log'))
for fpath in rawfiles:
    try:
        fname = osp.basename(fpath)
        date = datetime.strptime(fname[:11], "%b_%d_%Y")
        squeeze_met_data(fpath, date)
    except (IndexError, ValueError):
        print "Skipping unrecognizable file:", fname







