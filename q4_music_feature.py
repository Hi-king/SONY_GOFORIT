#!/usr/bin/python
# -*- coding:utf-8 -*-

DOC='''
=============================================================
 q4_music_feature.py
-------------------------------------------------------------
 arguments
    |- 1.targetmusicstring
    |- (2.targetnote)
        |- default : None
 output
    |- feature = $(feature)
    |- (if targetnote )
         |- answer melody is..
         |- $(melody)
 example
    |- $ q4_music_feature.py 3:4:,2:4:,1:4:,0:4:,1:4:,2:4:,3:4:,:4:,1:8:,0:4.:,-1:4:,-2:4:,:8:,-1:4.:,0:8:,1:8:
         |- output : 
             |- feature= 24
    |- $ q4_music_feature.py 3:4:,2:4:,1:4:,0:4:,1:4:,2:4:,3:4:,:4:,1:8:,0:4.:,-1:4:,-2:4:,:8:,-1:4.:,0:8:,1:8:
         |- output : 
             |- feature= 24
             |- answer melody is...
             |- 3:4:,2:4:,3:4:,3:4:b,2:4:,3:4:,2:4:,:4:,4:8:s,4:4.:,3:4:b,4:4:,:8:,3:4.:b,4:8:,3:8:
    |- $ ./q4_music_feature.py 3:4:,2:4:,3:4:,3:4:b,2:4:,3:4:,2:4:,:4:,4:8:s,4:4.:,3:4:b,4:4:,:8:,3:4.:b,4:8:,3:8:
         |- output :
             |- feature= 24


-------------------------------------------------------------
 for Python 2.7
 K.Ogaki(ogaki@iis.u-tokyo.ac.jp)
 2012/02/07
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

# ==============
#  音符間の距離
# ==============
def notesdistance(note1, note2):
    if(int(note1[0])>int(note2[0])):
        return notetonote(note2, note1)
    elif(int(note1[0])<int(note2[0])):
        return notetonote(note1, note2)
    else:
        dist = 0
        if note1[2] == "s":
            dist -= 1
        elif note1[2] == "x":
            dist -= 2
        elif note1[2] == "b":
            dist +=1
        elif note1[2] == "d":
            dist +=2
            
        if note2[2] == "s":
            dist += 1
        elif note2[2] == "x":
            dist += 2
        elif note2[2] == "b":
            dist -=1
        elif note2[2] == "d":
            dist -=2

        if(dist>=0):
            return notetonote(note1, note2)
        else:
            return notetonote(note2, note1)

def notetonote(note1, note2):
    dist = 0
    for i in xrange(int(note1[0]), int(note2[0]) ):
        octnote = i%7
        if(octnote == 0 or octnote == 3):
            dist += 1
        else:
            dist += 2

    # --- accidental ---
    if note1[2] == "s":
        dist -= 1
    elif note1[2] == "x":
        dist -= 2
    elif note1[2] == "b":
        dist +=1
    elif note1[2] == "d":
        dist +=2

    if note2[2] == "s":
        dist += 1
    elif note2[2] == "x":
        dist += 2
    elif note2[2] == "b":
        dist -=1
    elif note2[2] == "d":
        dist -=2

    return abs(dist)

def musiclist_to_string(musiclist):
    musicstring = ""
    for item in musiclist:
        musicstring+=(item[0]+":"+item[1]+":"+item[2]+",")
    return musicstring[:-1]
def musicstring_to_list(musicstring):
    return [ [ item for item in note.split(":") ] for note in musicstring.split(",") ]
def calcfeature(musicstring):
    mlist = musicstring_to_list(musicstring)
    features = []
    for i in xrange(len(mlist)-1):
        if(mlist[i][0]==''): # rest note
            continue

        nexti = i+1
        while(nexti<len(mlist) and mlist[nexti][0]==''): #rest note
            nexti+=1
        if(nexti==len(mlist)):
            break
        
        features.append( notesdistance(mlist[i], mlist[nexti]) )
    return features

# ==========================
#  音符をshift*半音分ずらす
# ==========================
def shiftnote(nownote, shift):
    if nownote[2] == "s":
        shift += 1
    elif nownote[2] == "x":
        shift += 2
    elif nownote[2] == "b":
        shift -=1
    elif nownote[2] == "d":
        shift -=2

    retnote = [nownote[0], nownote[1], '']
    return shiftnotesub(retnote, shift)

def shiftnotesub(nownote, shift):
    intnote = int(nownote[0])
    octnote = intnote % 7
    if(shift==0):
        return nownote
    if(shift>=0):
        if(octnote == 0 or octnote == 3):
            nownote[0] = str(intnote+1)
            return shiftnotesub(nownote, shift-1)
        else:
            if(shift>=2):
                nownote[0] = str(intnote+1)
                return shiftnotesub(nownote, shift-2)
            else:
                nownote[2] = "s"
                return shiftnotesub(nownote, shift-1)
    else:
        if(octnote == 1 or octnote == 4):
            nownote[0] = str(intnote-1)
            return shiftnotesub(nownote, shift+1)
        else:
            if(shift<=-2):
                nownote[0] = str(intnote-1)
                return shiftnotesub(nownote, shift+2)
            else:
                nownote[2] = "b"
                return shiftnotesub(nownote, shift+1)

# =================
#  priority search
# =================
import heapq
class searchitem(object):
    def __init__(self, note, path):
        self.note = note
        self.path = path
        self.distance = notesdistance(self.note, [targetnote, '', ''] )
    def __le__(self, other):
        return self.distance < other.distance
       
def searchmelody(musicstring):
    mlist = musicstring_to_list(musicstring)
    targetdists = calcfeature(musicstring)
    
    queue = [searchitem(mlist[0], [])]
    while(1):
        nowsearchitem = heapq.heappop(queue)
        if(len(nowsearchitem.path)==len(targetdists)):
            if(nowsearchitem.note[0] == targetnote):
                break
        else:
            #print nowsearchitem.path
            shift = targetdists[len(nowsearchitem.path)]
            heapq.heappush(queue, searchitem( shiftnote(nowsearchitem.note, +shift), nowsearchitem.path+["+"] ) )
            heapq.heappush(queue, searchitem( shiftnote(nowsearchitem.note, -shift), nowsearchitem.path+["-"] ) )
    
    anspath = nowsearchitem.path
    #print anspath
    returnlist = [ mlist[0] ]
    nownote = mlist[0]
    j=0
    for i in range(len(mlist)-1):
        if(mlist[i+1][0] == ''): ## rest note
            returnlist.append(mlist[i+1])
        else:
            if(anspath[j]=="+"):
                nownote = shiftnote(nownote, +targetdists[j])
            else:
                nownote = shiftnote(nownote, -targetdists[j])
            nownote[1]=mlist[i+1][1] ## duration
            returnlist.append(nownote)
            j+=1
    
    return returnlist
# ======
#  main
# ======
targetnote = '-2'

if __name__ == '__main__':
    # --- argument check ---
    if(len(sys.argv) > 1):
        musicstring = sys.argv[1]
    else:
        print "error : need more arguments"
        print DOC
        exit(1)
    
    print "feature=",sum(calcfeature(musicstring))

    if(len(sys.argv) > 2):
        targetnote = sys.argv[2]
        anslist =  searchmelody(sys.argv[1])
        print "answer melody is..."
        print musiclist_to_string(anslist)

    exit(0)

