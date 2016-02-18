import test_frame as tf
from test_frame import makeTest
import dbmanager
import requests
import json
import sys

ADD_APP_URL = 		tf.HOST + '/application'
ALL_APP_URL = 		tf.HOST + '/applications'
new_app_data = {}

def addApplication(session, data):
	new_app_data['title'] = data
	t = session.post(ADD_APP_URL, headers = tf.HEADERS, data = json.dumps(new_app_data))
	return t

def getAllApplicationsFromAPI():
	session = tf.login()
	t = session.get(ALL_APP_URL, headers = tf.HEADERS)
	return t.json()



@makeTest
def addAppOK():
	session = tf.login()
	response = addApplication(session,tf.titleGenerator(5))
	app = response.json()['app']

	connection = dbmanager.connect()
	dbObject = dbmanager.getApplicationById(app,connection)


	if (dbObject == None):
		raise Exception('Object is not present on db!!')

	allApps = getAllApplicationsFromAPI()
	found = False
	for a in allApps:
		if a == app:
			found = True
	if not found:
		raise Exception('id is not returned by api')


@makeTest
def addAppNoTitle():
	session = tf.login()
	response = addApplication(session,None)
	if not response.status_code == 400:
		raise Exception('test not passed, Status Code different from 400')

@makeTest
def addAppNoLogin():
	new_app_data['title'] = tf.titleGenerator(5)
	t = requests.post(ADD_APP_URL, headers = tf.HEADERS, data = json.dumps(new_app_data))
	if not t.status_code == 401:
		raise Exception('test not passed, Status Code different from 401')
	
if __name__ == "__main__":
	addAppOK()
	addAppNoTitle()
	addAppNoLogin()





