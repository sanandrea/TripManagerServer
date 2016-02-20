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
        if str(i) in cDict:
            customer = sjson.loads(cDict[str(i)])
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