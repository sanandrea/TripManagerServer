import test_frame as TF
from test_frame import makeTest
import requests
import string
import json
import sys

PASSWORD = "test"
BASE_URL = TF.HOST + "/api/v1"
REGISTER_URL = BASE_URL + "/Customers"
LOGIN_URL = BASE_URL + "/Customers/login"

@makeTest
def testRegister():
    username = TF.titleGenerator(5,string.ascii_lowercase)
    password = PASSWORD
    try:
        register_info = {
            'username' : username,
            'password' : password
        }
        q = requests.post(REGISTER_URL,data = register_info)
        
        if q.status_code != 200:
            raise Exception('Wrong status code')
        
        result = q.json()

        if (result['username'] == None):
            raise Exception('No username returned')
        if (result['id'] == None):
            raise Exception('No id returned')

    except requests.exceptions.ConnectionError:
        print "Ooops server not available!"
        exit(100)


@makeTest
def testLogin():
  loginUser()


def loginUser():
    try:
        login_info = {
            'username' : 'zirvt',
            'password' : PASSWORD
        }
        q = requests.post(LOGIN_URL,data = login_info)
        
        if q.status_code != 200:
            raise Exception('Wrong status code')
        
        result = q.json()

        if (result['userId'] == None):
            raise Exception('No userId returned')
        if (result['id'] == None):
            raise Exception('No cookie returned')

        return result['id']

    except requests.exceptions.ConnectionError:
        print "Ooops server not available!"
        exit(100)

if __name__ == "__main__":
    testRegister()
    testLogin()
