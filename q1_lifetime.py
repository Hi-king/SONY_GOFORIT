#!/usr/bin/python
# -*- coding:utf-8 -*-

DOC='''
=============================================================
 lifetime.py
-------------------------------------------------------------
 arguments
    |- 1.today : YYYY/MM/DD
    |- 2.life duration
    |- (3.today : YYYY/MM/DD)
        |- default : 2012/02/06
 output
    |- "today is $(hour):$(minutes):$(second) in your life"
 example
    |- $ lifetime.py 2000/01/01 80
        |- output : "today is 3:39:4 in your life"
-------------------------------------------------------------
 for Python 2.7
 K.Ogaki(ogaki@iis.u-tokyo.ac.jp)
 2012/02/06
-------------------------------------------------------------
 This program is released under GPL.
 http://www.opensource.jp/gpl/gpl.ja.html.euc-jp
=============================================================
'''
GPL='''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import math

# ===================================
#  year年の1月から12月の日数のリスト
# ===================================
def daysinmonth(year):
    list_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    if( (year%4==0 and year%100!=0) or year%400==0):
            list_days[1]=29
    return list_days

# ===========================
#  enddate-startdateの総日数
# ===========================
def howmanydays(startdate, enddate):
    alltime = sum([sum(daysinmonth(year)) for year in xrange(startdate[0]+1, enddate[0])])
 
    if(startdate[0]==enddate[0]): #thisyear is birthyear
        alltime += sum([ daysinmonth(startdate[0])[i] for i in xrange(startdate[1]-1, enddate[1]-1) ])
        if(startdate[1]==enddate[1]): #enddate is birth month
            alltime += enddate[2]-startdate[2]
        else:
            alltime += ( daysinmonth(startdate[0])[ startdate[1]-1 ] - startdate[2] )
            alltime += enddate[2]
    else:
        # --- birthyear ---
        alltime += sum([ daysinmonth(startdate[0])[i] for i in xrange(startdate[1]-1, 12) ])
        alltime += ( daysinmonth(startdate[0])[ startdate[1]-1 ] - startdate[2] )
 
        # --- thisyear ---
        alltime += sum([ daysinmonth(enddate[0])[i] for i in xrange(enddate[1]-1)])
        alltime += enddate[2]
        
    return alltime

# ======
#  解答
# ======
def lifetime(birthday, duration, today):
    endday = [birthday[0]+duration, birthday[1], birthday[2] ] 
    floattimes = (24.0*howmanydays(birthday, today)) / howmanydays(birthday, endday)

    # --- hours ---
    anstime = []
    anstime.append( math.floor(floattimes) )
    # --- minutes ---
    floattimes = floattimes - anstime[0]
    floattimes *= 60
    anstime.append( math.floor(floattimes) ) 
    # --- seconds --- 
    floattimes = floattimes - anstime[1]
    floattimes *= 60
    anstime.append( int(floattimes) )

    return anstime
    
# ======
#  main
# ======
if __name__ == '__main__':

    # --- argument check ---
    if(len(sys.argv) >= 3):
        birthday = [ int(item) for item in sys.argv[1].split("/") ]
        lifeduration = int(sys.argv[2])
    else:
        print "error : need more arguments"
        print DOC
        exit(1)
    today = [ 2012, 02, 06 ]
    if(len(sys.argv) >= 4):
        today = [ int(item) for item in sys.argv[3].split("/") ]
    
    # --- print answer ---
    times = lifetime(birthday, lifeduration, today)
    print "today is %d:%d:%d in your life" % ( times[0], times[1], times[2] )


