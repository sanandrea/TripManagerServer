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
import requests
import json
import os
import re
import string
import random
import sys



HOST_LOCAL = 'http://127.0.0.1:3000'
#HOST_REMOTE = 'http://photogallery-sanandrea.rhcloud.com'

debug = os.environ['DEBUG']

if debug == "1":
    DEBUG = True
    HOST = HOST_LOCAL
else:
    DEBUG = False
    HOST = HOST_REMOTE

HEADERS = {
    'Content-Type' : 'application/json'
}





class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def titleGenerator(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

def camel_case_split(identifier):
    return re.sub("([a-z])([A-Z])","\g<1> \g<2>",identifier)

def makeTest(fn, *args, **kwargs):
    def wrapped(*args, **kwargs):
        print "\n=== Begin " + camel_case_split(fn.__name__) + " ==="
        try:
            result = fn(*args, **kwargs)
            print 'Test ' + bcolors.OKBLUE + " Passed " + bcolors.ENDC
            return result

        except Exception as e:
            print 'Test ' + fn.__name__ + bcolors.FAIL + bcolors.BOLD + " NOT PASSED! " + bcolors.ENDC + str(e) #+ sys.exc_info()[-1].print_stack()
            sys.exit(100)

    return wrapped



