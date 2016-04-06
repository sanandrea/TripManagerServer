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
#!/bin/bash
if [ $# == 0 ]
then
	echo "insert argument 0 for DEV, 1 for PROD"
	exit
fi

if [ $1 == 0 ]
then
	echo "Checking development system"
	export DEBUG="1"
else
	echo "Checking production system"
	echo "Stopping local node instance"
	killall node
	echo "Enable port forward..."
	rhc port-forward photogallery&
	RUBY_PID=$!
	sleep 8
	export DEBUG="0"
fi


for f in test_*.py
do
	python $f
	if [ $? != 0 ]
	then
		ERROR="1"
		break
	fi
done

if [[ $ERROR = "1" ]]
then
	printf 'Tests are \e[1;31m INTERRUPTED! \e[0m\n'
else
	printf 'All test \e[1;32m PASSED! \e[0m\n'
fi


if [ $1 == 1 ]
then
	echo "clean environment"
	kill $RUBY_PID
fi
