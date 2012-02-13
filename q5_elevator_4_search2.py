#!/usr/bin/python
# -*- coding:utf-8 -*-

DOC='''
=============================================================
 q5_elevator_4_search2.py
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
 2012/02/13
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
I_MOVE_ELEVATOR_ID = 0
I_MOVE_NOW = 1
I_MOVE_FLOOR = 2
I_MOVE_OPEN_CLOSE = 3
I_MOVE_PERSON1 = 4
I_MOVE_PERSON2 = 5
I_MOVE_PERSON3 = 6
I_MOVE_PERSON4 = 7
I_MOVE_PERSON5 = 8
I_CALL_ID = 0
I_CALL_TIME = 1
I_CALL_FLOOR_RIDE = 2
I_CALL_FLOOR_DROP = 3

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
        self.opentime = -5
        self.callindexs = [num-1]
        self.passangers = []
    def open(self, unload_list, outlist=None):
        self.opentime = self.now
        for passanger in [ item for item in unload_list if item>0 ]:
            self.passangers.remove(passanger)
            allpassangers.remove(passanger)
        if(outlist!=None):
            templist = [ self.number, self.now, self.floor, 'B', 0, 0, 0, 0, 0]
            templist[4:4+len(unload_list)] = unload_list
            outlist.append(templist)
    def close(self, load_list, outlist=None):
        self.opentime = -1
        self.passangers+=([item for item in load_list if item>0])
        if(outlist!=None):
            templist = [ self.number, self.now, self.floor, 'E', 0, 0, 0, 0, 0]
            templist[4:4+len(load_list)] = load_list
            outlist.append(templist)
# =====================
#  assign next index
# =====================
nextcallindex = 2
def assignindexs(elevators, calldata):
    global nextcallindex

    while( ( (not elevators[0].callindexs) or (not elevators[1].callindexs) ) and nextcallindex<(len(calldata)-1) ):
        if(abs(calldata[nextcallindex][I_CALL_FLOOR_RIDE]-elevators[0].floor) == abs(calldata[nextcallindex][I_CALL_FLOOR_RIDE]-elevators[1].floor)):
            if(len(elevators[1].callindexs)>len(elevators[0].callindexs)):
                elevators[0].callindexs.append(nextcallindex)
            else:
                elevators[1].callindexs.append(nextcallindex)
        elif(abs(calldata[nextcallindex][I_CALL_FLOOR_RIDE]-elevators[0].floor) > abs(calldata[nextcallindex][I_CALL_FLOOR_RIDE]-elevators[1].floor)):
            elevators[1].callindexs.append(nextcallindex)
        else:
            elevators[0].callindexs.append(nextcallindex)
        nextcallindex+=1
        #print "next",nextcallindex

    if(nextcallindex == len(calldata)-1):
        ## --- dummy call ---
        elevators[0].callindexs.append(len(calldata)-1)
        elevators[1].callindexs.append(len(calldata)-1)



# ====================
#  Search better path
# ====================
def search(outlist, calldata):
    ## --- dummy call ---
    calldata.append([len(calldata)+1, 100000000, 1, 1])

    elevators = [elevator(1), elevator(2)]
    while(1):
        if(not allpassangers): ## exit
            return 0
        #if(now<nowelevator.opentime+5):
        #    now = nowelevator.opentime+5

        if(elevators[0].now>=elevators[1].now):
            nowelevator = elevators[1]
        else:
            nowelevator = elevators[0]


        #print nowelevator.number
        #print nowelevator.passangers
        #print nowelevator.callindexs
        #print ""
   #print nowelevator.floor
        
        if(calldata[nowelevator.callindexs[0]][I_CALL_TIME]-abs(calldata[nowelevator.callindexs[0]][I_CALL_FLOOR_RIDE]-nowelevator.floor)*2 <= nowelevator.now):
            if(len(nowelevator.passangers)==0):
                if(nowelevator.floor == calldata[nowelevator.callindexs[0]][I_CALL_FLOOR_RIDE]):
                    ## --- arrived  --- ##
                    if(nowelevator.opentime<0):
                        ## --- open, ride, close --- ##
                        nowelevator.opentime = nowelevator.now
                        nowelevator.open([], outlist)

                    while(calldata[nowelevator.callindexs[0]][I_CALL_TIME]>nowelevator.now or nowelevator.now<nowelevator.opentime+5):
                        nowelevator.now+=1
                    nowelevator.close([calldata[nowelevator.callindexs[0]][I_CALL_ID]], outlist)
                    nowelevator.callindexs.pop(0)
                    assignindexs(elevators, calldata)

                elif(nowelevator.floor < calldata[nowelevator.callindexs[0]][I_CALL_FLOOR_RIDE]):
                    nowelevator.floor+=1
                    nowelevator.now+=2
                else:
                    nowelevator.floor-=1
                    nowelevator.now+=2
            else:
                ## --- 1-5 passangers ---
                direction = 0.0
                for i in nowelevator.passangers :
                    if calldata[i-1][I_CALL_FLOOR_DROP]!=nowelevator.floor:
                        direction += 1.0 / (calldata[i-1][I_CALL_FLOOR_DROP]-nowelevator.floor)
                
                if(len(nowelevator.passangers)!=5 and nowelevator.floor == calldata[nowelevator.callindexs[0]][I_CALL_FLOOR_RIDE] and direction * (calldata[nowelevator.callindexs[0]][I_CALL_FLOOR_DROP]-nowelevator.floor) > 0): ## ride
                    if(nowelevator.opentime<0):
                        ## --- open --- ##
                        nowelevator.opentime = nowelevator.now
                        nowelevator.open([], outlist)                    
                    while(calldata[nowelevator.callindexs[0]][I_CALL_TIME]>nowelevator.now or nowelevator.now<nowelevator.opentime+5):
                        nowelevator.now+=1
                    nowelevator.close([calldata[nowelevator.callindexs[0]][I_CALL_ID]], outlist)
                    nowelevator.callindexs.pop(0)
                    assignindexs(elevators, calldata)

                elif([1 for i in nowelevator.passangers if calldata[i-1][I_CALL_FLOOR_DROP] == nowelevator.floor]): ## drop
                    nowelevator.open([ passanger for passanger in nowelevator.passangers if calldata[passanger-1][I_CALL_FLOOR_DROP] == nowelevator.floor], outlist)
                    nowelevator.opentime = nowelevator.now
                    nowelevator.now+=5
                    nowelevator.close([], outlist)
                        
                else:  ## move
                    if(direction>=0):
                        nowelevator.floor += 1
                        nowelevator.now+=2
                    else:
                        nowelevator.floor -= 1
                        nowelevator.now+=2
        else: ## move
            direction = 0.0
            for i in nowelevator.passangers:
                if calldata[i-1][I_CALL_FLOOR_DROP]!=nowelevator.floor:
                    direction += 1.0 / (calldata[i-1][I_CALL_FLOOR_DROP]-nowelevator.floor)


            if([1 for i in nowelevator.passangers if calldata[i-1][I_CALL_FLOOR_DROP] == nowelevator.floor]): ## drop
                nowelevator.open([ passanger for passanger in nowelevator.passangers if calldata[passanger-1][I_CALL_FLOOR_DROP] == nowelevator.floor], outlist)
                nowelevator.opentime = nowelevator.now
                nowelevator.now+=5
                nowelevator.close([], outlist)
            else:  ## move
                if(direction>=0):
                    nowelevator.floor += 1
                    nowelevator.now+=2
                else:
                    nowelevator.floor -= 1
                    nowelevator.now+=2

# ======
#  main
# ======
if __name__ == '__main__':
    # --- argument check ---
    if(len(sys.argv) > 1):
        filename_call = sys.argv[1]
    else:
        print "error : need more arguments"
        1print DOC
        exit(1)

    calldata = [ [ int(item) for item in line.rstrip().split(",") ] for line in open(filename_call) ]
    #print calldata

    allpassangers = [ item[I_CALL_ID] for item in calldata]

    outlist = []
    search(outlist, calldata)
    #print outlist
    list_to_print(outlist)

    exit(0)
