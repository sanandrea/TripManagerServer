import test_frame as TF
from test_frame import makeTest
import requests
import string
import json
import sys
import datetime

PASSWORD = "test"
BASE_URL = TF.HOST + "/api/v1"
TRIP_URL = BASE_URL + "/Trips"

token = "aQVVwuBq4FaLdZO3sJhgfJprzBnrv5XAaAckMifYf5nXiLdWvg3xfpN64wDsH17D"

@makeTest
def testCreateTrip():
	dest = TF.titleGenerator(3)
	sd = datetime.datetime.now().isoformat()
	ed = datetime.datetime.now().isoformat()
	headers = TF.HEADERS
	headers['Authorization'] = token
	trip_data = {
		"destination" : dest,
		"startdate" : sd,
		"enddate" : sd,
		"comment" : "I love science!"
	}

	r = requests.post(TRIP_URL,headers = headers, data = json.dumps(trip_data))

	if (r.status_code != 200):
		raise Exception('Could not create trip',r.text)
	
	
if __name__ == "__main__":
	testCreateTrip()






