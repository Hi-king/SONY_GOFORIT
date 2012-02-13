#!/usr/bin/python
# -*- coding:utf-8 -*-

DOC='''
=============================================================
 q5_elevator_3_search.py
-------------------------------------------------------------
 arguments
    |- 1.input.csv
    |- 2.elevatormove.csv
 output
    |- Is Correct Move? :  $(True or False)
    |- Sum of All Cost is :  $sum
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
        self.opentime = -5
        self.passangers = []
    def open(self, unload_list, outlist=None):
        self.opentime = self.now
        for passanger in [ item for item in unload_list if item>0 ]:
            self.passangers.remove(passanger)
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

# ================
#  checker class
# ================
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
class elevator_checker(object):
    def __init__(self, movelist, calldata):
        #print "check"
        self.calldata = calldata
        self.movelist = movelist
        self.cost = 0
        self.passangerslist = [ line[0] for line in calldata ]

    ## --- move check ---
    def is_correct_moves(self):
        elevatornum = max([ line[0] for line in self.movelist ])
        test = elevator(1)
        self.elevators = [ elevator(i+1) for i in xrange(elevatornum) ]

        ## --- check and move ---
        for line in self.movelist:
            #print line
            if(line[I_MOVE_OPEN_CLOSE] == 'B'):
                if(self.can_open(line) and self.can_drop(line)):
                    self.elevators[line[I_MOVE_ELEVATOR_ID]-1].now = line[I_MOVE_NOW]
                    self.elevators[line[I_MOVE_ELEVATOR_ID]-1].floor = line[I_MOVE_FLOOR]
                    self.elevators[line[I_MOVE_ELEVATOR_ID]-1].open(line[I_MOVE_PERSON1:])
                else:
                    print "elavator open failed"
                    return False
            else:
                if(self.can_close(line) and self.can_ride(line)):
                    self.elevators[line[I_MOVE_ELEVATOR_ID]-1].now = line[I_MOVE_NOW]
                    self.elevators[line[I_MOVE_ELEVATOR_ID]-1].close(line[I_MOVE_PERSON1:])
                    for passanger in [item for item in line[I_MOVE_PERSON1:] if item>0 ]:
                        self.passangerslist.remove(passanger)
                else:
                    print "elavator close failed"
                    return False
        ## --- check all passangers ---
        if(len(self.passangerslist)):
            print "passangers waiting.."
            print self.passangerslist
            return False
        for eachelevator in self.elevators:
            if(len(eachelevator.passangers)):
                print "remain in elevator"
                print eachelevator.passangers
                return False

        ## --- move correctly ---
        return True
    
    def can_close(self, line):
        nowelevator = self.elevators[ line[I_MOVE_ELEVATOR_ID]-1 ]
        ## --- basic check ---
        if(nowelevator.floor!=line[I_MOVE_FLOOR]):
            print "wrong floor"
            return False
        ## --- 5seconds open rule ---
        if(nowelevator.opentime==-1 or nowelevator.opentime>(line[I_MOVE_NOW]-5) ):
            print "wait 5seconds..."
            return False
        ## --- passanger num rule ---
        nextpassangers = [ item for item in line[I_MOVE_PERSON1:] if item>0 ]
        for passanger in nextpassangers:
            if(passanger in nowelevator.passangers): ## ids must be unique
                return False
        nextpassangernum = len(nowelevator.passangers) + len(nextpassangers)
        if(nextpassangernum > 5):
            "passangers > 5"
            return False

        return True
        
    def can_open(self, line):
        nowelevator = self.elevators[ line[I_MOVE_ELEVATOR_ID]-1 ]
        ## --- move speed rule ---
        if(abs(line[I_MOVE_FLOOR] - nowelevator.floor)*2 > (line[I_MOVE_NOW] - nowelevator.now) ):
            print "wrong floor"
            return False
        ## --- passanger num rule ---
        unloadpassangers = [ item for item in line[I_MOVE_PERSON1:] if item>0 ]
        for passanger in unloadpassangers:
            if(not passanger in nowelevator.passangers):
                print "no such passanger"
                return False
        nextpassangernum = len(nowelevator.passangers) - sum([ 1 for item in line[I_MOVE_PERSON1:] if item>0 ])
        if(nextpassangernum < 0):
            print "passangers < 0"
            return False

        ## --- calc cost ---
        for passanger in unloadpassangers:
            self.cost += (nowelevator.now - self.calldata[passanger-1][I_CALL_TIME])

        return True

    def can_ride(self, line):
        nowelevator = self.elevators[ line[I_MOVE_ELEVATOR_ID]-1 ]
        for passanger in [ item for item in line[I_MOVE_PERSON1:] if item>0 ]:
            if(self.calldata[passanger-1][I_CALL_FLOOR_RIDE] != line[I_MOVE_FLOOR]):
                print "wrong floor to ride"
                return False
            if(self.calldata[passanger-1][I_CALL_TIME]>line[I_MOVE_NOW]):
                print "too early to go"
                return False
            
        return True
    
    def can_drop(self, line):
        nowelevator = self.elevators[ line[I_MOVE_ELEVATOR_ID]-1 ]
        for passanger in [ item for item in line[I_MOVE_PERSON1:] if item>0 ]:
            if(self.calldata[passanger-1][I_CALL_FLOOR_DROP] != line[I_MOVE_FLOOR]):
                print "wrong floor to drop"
                return False
            
        return True
        

# ======
#  main
# ======
if __name__ == '__main__':
    # --- argument check ---
    if(len(sys.argv) > 2):
        filename_call = sys.argv[1]
        filename_move = sys.argv[2]
    else:
        print "error : need more arguments"
        print DOC
        exit(1)

    calldata = [ [ int(item) for item in line.rstrip().split(",") ] for line in open(filename_call) ]
    #print calldata
    
    movedata = []
    for line in open(filename_move):
        templine = []
        for item in line.rstrip().split(","):
            if(item!='B' and item != 'E'):
                templine.append(int(item))
            else:
                templine.append(item)
        movedata.append(templine)
    #print movedata

    
    passangerslist = [ line[0] for line in calldata]

    checker = elevator_checker(movedata, calldata)
    print "Is Correct Move? : ",checker.is_correct_moves()
    print "Sum of All Cost is : ",checker.cost
    exit(0)
