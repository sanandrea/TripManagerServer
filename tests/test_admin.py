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
def testGetTripList(uid,token, isAdmin):
    headers = TF.HEADERS
    headers['Authorization'] = token
    r = requests.get(TRIP_URL, headers= headers)
    #print r.json()
    if isAdmin:
        if (r.status_code != 200):
            raise Exception('Could not get Trip list from Admin',r.text)
    else:
        if (r.status_code != 401):
            raise Exception('Could get Trip list from NON Admin',r.text)


@makeTest
def testAdminCanListAccounts():
    user1 = DB.getAdminUser()
    token1 = DB.getTokenforUserId(user1['id'])
    if token1 == None:
        token1 = TU.loginUser(user1['username'])
    getCustomers(token1, True)


@makeTest
def testUserCanNotListAccounts():
    user = DB.getNormalUser()
    if user == None:
        TU.testRegister()
    user = DB.getNormalUser()
    token = DB.getTokenforUserId(user['id'])
    if token == None:
        token = TU.loginUser(user['username'])
    getCustomers(token, False)


def getCustomers(token,isAdmin):
    headers = TF.HEADERS
    headers['Authorization'] = token

    r = requests.get(USER_URL, headers = headers)
    if isAdmin:
        if (r.status_code != 200):
            raise Exception('Could not get Customer list from Admin',r.text)
    else:
        if (r.status_code != 401):
            raise Exception('Could get Customer list from NON Admin',r.text)


@makeTest
def testAdminCanPromote():
    user1 = DB.getAdminUser()
    token1 = DB.getTokenforUserId(user1['id'])
    if token1 == None:
        token1 = TU.loginUser(user1['username'])
    userToPromote = DB.getNormalUser()
    if userToPromote == None:
        TU.testRegister()
        userToPromote = DB.getNormalUser()
    promoteUser(token1,userToPromote,True)

@makeTest
def testUserCanNotPromote():
    user1 = DB.getNormalUser()
    token1 = DB.getTokenforUserId(user1['id'])
    if token1 == None:
        token1 = TU.loginUser(user1['username'])
    userToPromote = DB.getNormalUser()
    if userToPromote == None:
        TU.testRegister()
        userToPromote = DB.getNormalUser()
    promoteUser(token1,userToPromote,False)


def promoteUser(tokenOfCaller, userToPromote, isAllowed):
    headers = TF.HEADERS
    headers['Authorization'] = tokenOfCaller
    url = USER_URL + "/" + str(userToPromote['id']) + "/promote"
    r = requests.post(url, headers = headers)
    if isAllowed:
        if (r.status_code != 200):
            raise Exception('Could not Promote Customer from Admin',r.text)
    else:
        if (r.status_code != 401):
            raise Exception('Could promote Customer list from NON Admin',r.text)



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
    testGetTripList(user1,token1,True)
    testGetTripList(user2,token2, False)
    testAdminCanListAccounts()
    testUserCanNotListAccounts()
    testAdminCanPromote()
    testUserCanNotPromote()

