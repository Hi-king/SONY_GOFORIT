#!/usr/bin/python
# -*- coding:utf-8 -*-

DOC='''
=============================================================
 q5_elevator_1.py
-------------------------------------------------------------
 arguments
    |- 1.input.csv
 output
    |- Out1,Out2,Out3,Out4,Out5,Out6,Out7,Out8,Out9
    |- ....
        |-Out1 - エレベータの識別番号です。(1-)
        |-Out2 - エレベータの動作時刻です。開始してからの経過秒数で表します。(0-)
        |-Out3 - エレベータが動作した階です。(1-10)
        |-Out4 - エレベータの動作です。('B':開 'E':閉)
        |-Out5 - 入力データの識別番号1
        |-Out6 - 入力データの識別番号2
        |-Out7 - 入力データの識別番号3
        |-Out8 - 入力データの識別番号4
        |-Out9 - 入力データの識別番号5
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

# ===========
#  utilities
# ===========
def list_to_print(outlist):
    for line in outlist:
        for item in line[:-1]:
            sys.stdout.write(str(item)+",")
        print line[-1]


# ================
#  elevator class
# ================
class elevator(object):
    def __init__(self, num):
        self.number = num
        self.floor = 1
        self.now = 0
    def open(self, outlist, unload_list):
        templist = [ self.number, self.now, self.floor, 'B', 0, 0, 0, 0, 0]
        templist[4:4+len(unload_list)] = unload_list
        outlist.append(templist)
    def close(self, outlist, load_list):
        templist = [ self.number, self.now, self.floor, 'E', 0, 0, 0, 0, 0]
        templist[4:4+len(load_list)] = load_list
        outlist.append(templist)

# =================
#  simple elevator
# =================
def move_elevator_simple(inputdata):
    # --- init ---
    outlist = []
    elevator1 = elevator(1)
    elevator1.now = 0
    elevator1.floor = 1
    elevator1.close(outlist, [])

    # --- data processing ---
    for line in inputdata:
        # --- move to floor ---
        elevator1.now += abs(line[2] - elevator1.floor)*2
        elevator1.floor = line[2]
        elevator1.open(outlist, [])
        # --- loading ---
        elevator1.now = max([ elevator1.now+5, line[1] ])
        elevator1.close(outlist, [ line[0] ])
        # --- move to floor ---
        elevator1.now += abs(line[3] - elevator1.floor)*2
        elevator1.floor = line[3]
        elevator1.open(outlist, [line[0] ] )
        elevator1.now += 5
        elevator1.close(outlist, [])

    return outlist

# ======
#  main
# ======
targetnote = '-2'

if __name__ == '__main__':
    # --- argument check ---
    if(len(sys.argv) > 1):
        filename = sys.argv[1]
    else:
        print "error : need more arguments"
        print DOC
        exit(1)

    inputdata = [ [ int(item) for item in line.rstrip().split(",") ] for line in open(filename) ]
    #print inputdata
    outlist = move_elevator_simple(inputdata)
    list_to_print(outlist)

    exit(0)


    
    print "feature=",sum(calcfeature(musicstring))

    if(len(sys.argv) > 2):
        targetnote = sys.argv[2]
        anslist =  searchmelody(sys.argv[1])
        print "answer melody is..."
        print musiclist_to_string(anslist)

    exit(0)

