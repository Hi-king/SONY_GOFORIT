#!/usr/bin/python
# -*- coding:utf-8 -*-

DOC='''
=============================================================
 q2_gamma.py
-------------------------------------------------------------
 arguments
    |- 1.target : YYYY/MM/DD
    |- (2.alpha)
        |- default : 1000000
 output
    |- answer= $(target!)
    |- time= $(hour):$(minute):$(second)
 example
    |- $ q2_gamma.py 2.5 1000000
        |- output : "answer= 3.3233506936 \n time= 0:00:01.366805"
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
from datetime import datetime

def stirling_approximation(z):
    return math.sqrt(2*math.pi*z)*( (z/math.exp(1))**z )

def stirling_approximation_plus(z, alpha):
    ## stirling_approximation(z+alpha)/(z+1 * z+2 * ... * z+alpha)
    ## gamma(z) = gamma(z+1)/(z+1)
    nowdivisor = z+alpha
    nowdivisor_int = math.floor(z+alpha)
    nowdivisor_rest = z-math.floor(z)
    powcount = 0

    now = math.sqrt(2*math.pi*(z+alpha) )

    while( powcount<(z+alpha) and (nowdivisor_int+nowdivisor_rest)>=(z+1) ):
        if(now>10 or now<-10):
            now /= (nowdivisor_int+nowdivisor_rest)
            nowdivisor_int-=1
        else:
            now *= ( (z+alpha)/math.exp(1) )
            powcount += 1
    # ---  rest ---
    while((nowdivisor_int+nowdivisor_rest)>=(z+1)):
        now /= (nowdivisor_int+nowdivisor_rest)
        nowdivisor_int -= 1
    now *= ( (z+alpha)/math.exp(1) )**(z+alpha-powcount)

    return now

# ======
#  main
# ======
if __name__ == '__main__':

    # --- argument check ---
    if(len(sys.argv) > 1):
        target = float(sys.argv[1])
    else:
        print "error : need more arguments"
        print DOC
        exit(1)
    iternum = 1000000
    if(len(sys.argv) > 2):
        iternum = int(sys.argv[2])

    # --- print answer and time ---        
    time_s = datetime.now()
    print "answer=",stirling_approximation_plus(target, iternum)
    time_e = datetime.now()
    print "time=",time_e-time_s

    exit(0)
