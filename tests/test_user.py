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
            raise Exception('Wrong status code ', q.status_code, q.text)
        
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
