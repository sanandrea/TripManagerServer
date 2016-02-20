import test_frame as TF
from test_frame import makeTest
import requests
import string
import json
import sys
import datetime
import db_manager as DB
import test_user as TU


PASSWORD = "test"
BASE_URL = TF.HOST + "/api/v1"
TRIP_URL = BASE_URL + "/Trips"
USER_URL = BASE_URL + "/Customers"


@makeTest
def testCreateTripAdmin(token):
    createTrip(token)

def createTrip(token):
    dest = TF.titleGenerator(3)
    sd = datetime.datetime.now().isoformat()
    ed = datetime.datetime.now().isoformat()
    headers = TF.HEADERS
    auth = token

    headers['Authorization'] = auth
    trip_data = {
        "destination" : dest,
        "startdate" : sd,
        "enddate" : sd,
        "comment" : "I love science!"
    }

    r = requests.post(TRIP_URL,headers = headers, data = json.dumps(trip_data))
    
    if (r.status_code != 200):
        raise Exception('Could not create trip',r.text)

    return r.json()['id']

@makeTest
def testReadTripFromAdmin(token, tripId):
    headers = TF.HEADERS
    headers['Authorization'] = token

    r = requests.get(TRIP_URL + "/" + str(tripId), headers = headers)
    if (r.status_code != 200):
        raise Exception('Could not read trip from Admin',r.text)

@makeTest
def testUpdateTripFromAdmin(token, tripId):
    headers = TF.HEADERS
    headers['Authorization'] = token
    data = {"startdate" : datetime.datetime.now().isoformat()}
    r = requests.put(TRIP_URL + "/" + str(tripId), headers = headers)
    if (r.status_code != 200):
        raise Exception('Could not update trip from Admin',r.text)

@makeTest
def testDeleteTripFromAdmin(token, tripId):
    headers = TF.HEADERS
    headers['Authorization'] = token
    data = {"startdate" : datetime.datetime.now().isoformat()}
    r = requests.delete(TRIP_URL + "/" + str(tripId), headers = headers)
    if (r.status_code != 200):
        raise Exception('Could not delete trip from Admin',r.text)

@makeTest
def testGetTripList(uid,token):
    headers = TF.HEADERS
    headers['Authorization'] = token
    r = requests.get(TRIP_URL, headers= headers)
    #print r.json()

    if (r.status_code != 200):
        raise Exception('Could not get trip list from Admin',r.text)

if __name__ == "__main__":
    user1 = DB.getAdminUser()
    token1 = DB.getTokenforUserId(user1['id'])
    if token1 == None:
        token1 = TU.loginUser(user1['username'])
    testCreateTripAdmin(token1)

    user2 = DB.getNormalUser()

    if user2 == None:
        TU.testRegister()
    user2 = DB.getNormalUser()

    token2 = DB.getTokenforUserId(user2['id'])
    if token2 == None:
        token2 = TU.loginUser(user2['username'])

    tid = createTrip(token2)
    testReadTripFromAdmin(token1,tid)
    testUpdateTripFromAdmin(token1,tid)
    testDeleteTripFromAdmin(token1, tid)

    testGetTripList(user1,token1)




