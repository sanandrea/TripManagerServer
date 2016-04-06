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

def getAToken():
	auth = DB.getLoginToken()
	if auth == None:
		user = DB.getNormalUser()
		if user == None:
			print "No users registered skipping test!"
			return None
		TU.loginUser(user['username'])
		print "User logged in!"
		auth = DB.getLoginToken()
	return auth

@makeTest
def testCreateTrip(token):
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
def testReadTripFromOwner(token, tripId):
	headers = TF.HEADERS
	headers['Authorization'] = token

	r = requests.get(TRIP_URL + "/" + str(tripId), headers = headers)
	if (r.status_code != 200):
		raise Exception('Could not read trip',r.text)

@makeTest
def testUpdateTripFromOwner(token, tripId):
	headers = TF.HEADERS
	headers['Authorization'] = token
	data = {"startdate" : datetime.datetime.now().isoformat()}
	r = requests.put(TRIP_URL + "/" + str(tripId), headers = headers)
	if (r.status_code != 200):
		raise Exception('Could not update trip',r.text)

@makeTest
def testDeleteTripFromOwner(token, tripId):
	headers = TF.HEADERS
	headers['Authorization'] = token
	data = {"startdate" : datetime.datetime.now().isoformat()}
	r = requests.delete(TRIP_URL + "/" + str(tripId), headers = headers)
	if (r.status_code != 200):
		raise Exception('Could not delete trip',r.text)



@makeTest
def testReadTripFromOther(token, tripId):
	headers = TF.HEADERS
	headers['Authorization'] = token

	r = requests.get(TRIP_URL + "/" + str(tripId), headers = headers)
	if (r.status_code != 401):
		raise Exception('Not owner read Trip',r.text)

@makeTest
def testUpdateTripFromOther(token, tripId):
	headers = TF.HEADERS
	headers['Authorization'] = token
	data = {"startdate" : datetime.datetime.now().isoformat()}
	r = requests.put(TRIP_URL + "/" + str(tripId), headers = headers)
	if (r.status_code != 401):
		raise Exception('Not owner updated Trip',r.text)

@makeTest
def testDeleteTripFromOther(token, tripId):
	headers = TF.HEADERS
	headers['Authorization'] = token
	data = {"startdate" : datetime.datetime.now().isoformat()}
	r = requests.delete(TRIP_URL + "/" + str(tripId), headers = headers)
	if (r.status_code != 401):
		raise Exception('Not owner deleted Trip',r.text)


@makeTest
def testGetTripList(uid,token):
	headers = TF.HEADERS
	headers['Authorization'] = token
	r = requests.get(USER_URL + "/" + str(uid) + "/trips", headers= headers)

	if (r.status_code != 200):
		raise Exception('Could not get trip list',r.text)

	
if __name__ == "__main__":
	user1 = DB.getNormalUser()
	token1 = DB.getTokenforUserId(user1['id'])
	if token1 == None:
		token1 = TU.loginUser(user1['username'])

	tid = testCreateTrip(token1)
	testReadTripFromOwner(token1,tid)
	testUpdateTripFromOwner(token1, tid)
	testDeleteTripFromOwner(token1, tid)


	user2 = DB.getNormalUser()
	

	while (user1['id'] == user2['id']):
		TU.testRegister()
		user2 = DB.getNormalUser()

	
	token2 = DB.getTokenforUserId(user2['id'])
	if token2 == None:
		token2 = TU.loginUser(user2['username'])
	tid = testCreateTrip(token1)
	testReadTripFromOther(token2,tid)
	testUpdateTripFromOther(token2,tid)
	testDeleteTripFromOther(token2, tid)

	

	testGetTripList(user1['id'], token1)





