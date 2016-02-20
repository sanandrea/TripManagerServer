import test_frame as TF
from test_frame import makeTest
import db_manager as DB
import requests
import string
import json
import sys

PASSWORD = "test"
BASE_URL = TF.HOST + "/api/v1"
REGISTER_URL = BASE_URL + "/Customers"
LOGIN_URL = BASE_URL + "/Customers/login"
LOGOUT_URL = BASE_URL + "/Customers/logout"
TOKEN = ''

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
  global TOKEN
  TOKEN = loginUser(DB.getNormalUser()['username'])


def loginUser(user):
    try:
        login_info = {
            'username' : user,
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


@makeTest
def testLogout():
  logoutUser()

def logoutUser():
    try:
        headers = TF.HEADERS
        headers['Authorization'] = TOKEN

        q = requests.post(LOGOUT_URL, headers = headers)
        if q.status_code != 204:
            raise Exception('Wrong status code', q.text)

    except requests.exceptions.ConnectionError:
        print "Ooops server not available!"
        exit(100)


if __name__ == "__main__":
    testRegister()
    testLogin()
    testLogout()
