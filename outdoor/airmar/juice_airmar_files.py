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
columns = [('TIMESTAMP',      'GMT-8'),
           ('m200WX_P',       'mbar'),
           ('m200WX_T',       'degC'),
           ('m200WX_RH',      '%'),
           ('m200WX_dew_T',   'degC'),
           ('m200WX_WD_true', 'degEofTN'),
           ('m200WX_WD_mag',  'degEofMN'),
           ('m200WX_WS',      'm/s')]
col_names = ','.join(['"%s"' % ea[0] for ea in columns])
col_units = ','.join(['"%s"' % ea[1] for ea in columns])


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
            outfile.write(col_names+'\n')
            outfile.write(col_units+'\n')
            for line in datafile:
                #each data protocol key is divided by a $ identifier
                time, data = line.split('$')
                timestamp = date.strftime('"%Y-%m-%d ' + time[:-5] + '"' )
                #WIMDA is data protocol key for the meteorological composite
                if data.startswith('WIMDA'):
                    (key, bpi, bpiu, bp, bpbu, at, atu, wt, wtu,
                     rh, ah, dp, dpu, wdt, wdtu, wdm, wdmu, wsk,
                     wsku, wsm, wsmu) = data.split(',')
                    #convert barometric pressure (bars) to mbars
                    bp = "{:.1f}".format( float(bp)*1000 ) if bp else '"NAN"'
                    if not at: at = '"NAN"'
                    if not rh: rh = '"NAN"'
                    if not dp: dp = '"NAN"'
                    if not wdt: wdt = '"NAN"'
                    if not wdm: wdm = '"NAN"'
                    if not wsm: wsm = '"NAN"'
                    csvrec = ','.join([timestamp, bp, at, rh, dp, wdt, wdm, wsm])
                    outfile.write(csvrec+'\n')


rawfiles = glob(osp.join(args.source, '*.log'))
for fpath in rawfiles:
    try:
        fname = osp.basename(fpath)
        date = datetime.strptime(fname[:11], "%b_%d_%Y")
        squeeze_met_data(fpath, date)
    except (IndexError, ValueError):
        print "Skipping unrecognizable file:", fname







