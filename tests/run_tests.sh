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
