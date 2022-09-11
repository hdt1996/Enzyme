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

#Join Commands:
#	&& execute following after success of previous
#	& execute previous in background and following no matter result of previous
#	| execute previous and use output(stdout/echo) as input to following (auto-prompt)
#	|| execute following only if previous failed (returns nonzero code; zero = success) 

OPTIONS="-repo -user -branch"
BRANCH=""
REPO=""
USER=$(git config user.name)
DEST=$(git config user.destination)

#Function to handle passing non-kwarg/single arg that executables need for true/false
ARG_BOOL(){ 
	#ARGS
		#$1: Value arg passed in script: true or false | 0 or 1
		#$2: Dependency arg required for dependency executable i.e. -o -p -a etc.

	if [ $1 = 0 ]; then
		echo ""
	elif [ $1 = 1 ]; then
		echo "$2"
	else
		echo "ERROR: Unallowed Argument for BOOL TYPE"
		exit 1
	fi
}

#Function to handle passing kwargs that executables need
KWARG(){
	#ARGS
		#$1: Dependency arg required for dependency executable i.e. -password or -p
		#$2: Value arg passed in script: string or number
	echo "$1 $2"
		#Result should look like -password MyCustomPassword or -p MyCustomPassword
}

#Function to handle passing kwargs where value is key=value pair
KWARG_KEYEQVAL(){
	#ARGS
		#$3: Dependency arg required for dependency executable i.e. -password or -p
		#$1: Key arg from K=V pair (Named arg passed in script)
		#$2: Value arg from K=V pair (Value arg passed in script)
	echo "$3 $1=$2"
}

VARS_ASSIGN(){
	case $1 in
	-repo)
		REPO=$2;;
	-user)
		USER=$2;;
	-branch)
		BRANCH=$2;;
	esac
}

INDEX=0
CURR_VAR=""
for var in "$@"
do
	allowed=0
	echo "$var"
	for opt in $OPTIONS;
	do
		if [ "$var" = "$opt" ] && [ $INDEX = 0 ]; then
			allowed=1
			CURR_VAR="$var"
		fi
	done
	
	if [ $allowed = 0 ] && [ $INDEX = 0 ]; then
		echo "ERROR: Unallowed Argument ---> $var <---"
		exit 1
	elif [ $INDEX = 1 ]; then
		VARS_ASSIGN $CURR_VAR $var
		INDEX=$((0))
	else
		INDEX=$((INDEX+1))
	fi
	
done

echo "git push git@github.com:$USER/$REPO.git $BRANCH"
read x
cd $DEST/$REPO
git add --all .
#git reset HEAD^
git commit -m "Test commit"
git push git@github.com:$USER/$REPO.git main

read x

