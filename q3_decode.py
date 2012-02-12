#!/usr/bin/python
# -*- coding:utf-8 -*-

DOC='''
=============================================================
 q3_decode.py
-------------------------------------------------------------
 arguments
    |- (1.targetstring)
        |- default : sony
    |- (2.codestring)
        |- default : from problem 
 output
    |- skip[0],index[0]\n .... skip[n],index[n]\n
    |- time= $(hour):$(minute):$(second)
 example
    |- $ q3_decode.py 
    |- $ q3_decode.py sony ssoonnyy
-------------------------------------------------------------
 for Python 2.7
 K.Ogaki(ogaki@iis.u-tokyo.ac.jp)
 2012/02/10
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
# =================
#  code generation
# =================
def codegen():
    r = 16
    codestr = ""
    for i in xrange(300000):
        codestr += chr( 0x61 + ( 26 * ( r / 0x10000) ) / 0x10000 )
        r = ( r*1103515245 + 12345 ) & ( 0xFFFFFFFF )
    return codestr

# ============
#  searching
# ============
def search1(targetstr):
    list1 = [ i for i in xrange(len(codestr)) if codestr[i]==targetstr[0] ]
    list2 = [ i for i in xrange(len(codestr)) if codestr[i]==targetstr[1] ]
    anslist = []

    now=0
    for i1 in list1:
        #sys.stdout.write("\r%F" % (float(now)/len(list1)) )
        now+=1;
        for i2 in list2:
            if(istrueindex(i2, i2-i1, targetstr[2:])):
                if((i2-i1)>0):
                    anslist.append([i2-i1, i1])
                else:
                    anslist.append( [i1-i2, i1+(i2-i1)*(len(targetstr)-1) ])
    return anslist
            
def istrueindex(now, skip, targetstr):
    if( len(targetstr)==0 ):
        return True
    if( (now+skip)<0 or (now+skip)>=len(codestr)):
        return False

    if(codestr[now+skip]==targetstr[0]):
        return istrueindex(now+skip, skip, targetstr[1:])
    else:
        return False

# ======
#  main
# ======
codestr = ""
if __name__ == '__main__':

    # --- argument check ---
    targetstring = "sony"
    if(len(sys.argv) > 1):
        targetstring = sys.argv[1]

    if(len(sys.argv) > 2):
        codestr = sys.argv[2]
    else:
        codestr = codegen()

    # --- print answer and time ---        
    time_s = datetime.now()
    anslist = search1(targetstring)
    anslist.sort()
    time_e = datetime.now()
    for item in anslist:
        print item[0],",",item[1]
    print "time=",time_e-time_s
    print "ansnum=",len(anslist)
    exit(0)
