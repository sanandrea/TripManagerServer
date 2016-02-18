import requests
import json
import os
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

def makeTest(fn):
	def wrapped():
		print "\n=== Begin " + fn.__name__ + " test ==="
		try:
			fn()
			print "*** Passed " + fn.__name__ + " test ***"
			#sys.exit(0)
		except Exception as e:
			print 'Test ' + fn.__name__ + bcolors.FAIL + bcolors.BOLD + " NOT PASSED! " + bcolors.ENDC + str(e) #+ sys.exc_info()[-1].print_stack()
			sys.exit(100)

	return wrapped



