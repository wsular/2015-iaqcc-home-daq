# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os.path as osp
#import sys

#import glob
fpath = r'C:\Users\lar\Documents\Airmar WeatherCaster\WeatherCaster 3_005\Raw Data Log'
#files = glob.glob(fpath+'\*.log')
#for ea in files:
#    print ea

#if sys.argv[1]:
#    fname = sys.argv[1].strip('"')
#else:
fname = r'Jul_07_2015_3201670_0183.LOG'

#Date for the current file being processed. Be sure this accurately
#reflects the data. To be used with 'inputdate' variable.
YYYY_MM_DD = "2015-07-07" 

oname = "fixed_"+fname

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


with open(osp.join(fpath, oname), mode='w') as outfile:
   with open(osp.join(fpath, fname)) as datafile:              
        outfile.write(header)
        outfile.write(units)
        for line in datafile:
            #each data protocol key is divided by a $ identifier
            time, data = line.split('$')
            #autostamp rips date from file name
            autostamp = '"' + fname[:-17] + " " + time[:-5] + '"'
            #inputstamp uses date entered at top of code           
            inputstamp = '"' + YYYY_MM_DD + " " + time[:-5] + '"'
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
                dataout = (inputstamp + 
                        "," + bp + "," + at + "," + rh + 
                        "," + dp + "," + wdt + "," + wdm + 
                        "," + wsm +'\n')
                outfile.write(dataout)
            




