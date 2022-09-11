#!/bin/bash
#var OPTIONS -- Add Named Arguments Separated by Space
#Declare global vars after OPTIONS for use in executed command (Last Line)
#	Ex. USER=""
#	Ex. --CATEGORY=""   NOTE THE -- double hyphens included in argument!
#CASE_ASSIGN Function: 
#	Each case is specified per each named arguments (opt) in OPTIONS
#		Ex. USER) ...execution
#		Ex. --CATEGORY) ...execution
#	Execution of case: Update related global variable to $2
#		Ex. USER=$2
OPTIONS="-filename"
filename=""

CASE_ASSIGN(){
	case $1 in
	-filename)
		filename=$2;;
	esac
}

INDEX=0
CURR_VAR=""
for var in "$@"
do
	allowed=0
	for opt in $OPTIONS;
	do
		if [ "$var" = "$opt" ]; then
			allowed=1
			CURR_VAR="$var"
		fi
	done
	
	if [ $allowed = 0 ] && [ $INDEX = 0 ]; then
		echo "ERROR: Unallowed Argument ---> $var <---"
		exit 1
	elif [ $INDEX = 1 ]; then
		CASE_ASSIGN $CURR_VAR $var
		INDEX=$((0))
	else
		INDEX=$((INDEX+1))
	fi
	
done


echo "$filename"
cd ~/.ssh && mkdir ./tests & cd ~/.ssh && echo "./$filename" | ssh-keygen
ssh-add "$filename"
echo "Generated public key and installed private key!"

