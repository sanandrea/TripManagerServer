# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
#
#  Copyright © 2016 Andi Palo
#  This file is part of project: Simple Loopback Server
#
import json
from random import randint
import simplejson as sjson

def getDBJSON():
    with open('../db.json') as data_file:    
        return json.load(data_file)

def getNormalUser():
    db = getDBJSON()
    #one is the admin
    if len(db['models']['Customer']) < 2:
        return None

    while (True):
        index = randint(1, len(db['models']['Customer']))
        cList = db['models']['Customer']
        customer = sjson.loads(cList[str(index)])
        if customer['username'] != 'admin':
            return customer

def getAdminUser():
    db = getDBJSON()
    #one is the admin
    if len(db['models']['Customer']) == 0:
        return None
    cDict = db['models']['Customer']
    for i in range(0, len(cDict)):
        if str(i + 1) in cDict:
            customer = sjson.loads(cDict[str(i+1)])
            if customer['username'] == 'admin':
                return customer

def getLoginToken():
    db = getDBJSON()
    if len(db['models']['AccessToken']) == 0:
        return None
    keys = db['models']['AccessToken'].keys()
    return keys[0]

def getTokenforUserId(uid):
    db = getDBJSON()
    if len(db['models']['AccessToken']) == 0:
        return None
    
    for at,value in db['models']['AccessToken'].iteritems():
        entry = sjson.loads(value)
        if entry['userId'] == uid:
            return at
    return None



if __name__ == '__main__':
    print getNormalUser()
    print getAdminUser()
    print getLoginToken()