#!/bin/sh
sudo apt-get install git

BASEDIR=$(readlink -f $(dirname "$0"))
OPTIONS="-user -email -dest -backup"
BACKUP=""
DEST=""
USER=""
EMAIL=""

ARG_BOOL(){ 

	if [ $1 = 0 ]; then
		echo ""
	elif [ $1 = 1 ]; then
		echo "$2"
	else
		echo "ERROR: Unallowed Argument for BOOL TYPE"
		exit 1
	fi
}

KWARG(){
	echo "$1 $2"
}


KWARG_KEYEQVAL(){
	echo "$3 $1=$2"
}

VARS_ASSIGN(){
	case $1 in
	-dest)
		DESTINATION=$2;;
	-user)
		USER=$2;;
	-backup)
		BACKUP=$2;;
	-email)
		EMAIL=$2;;
	esac
}

INDEX=0
CURR_VAR=""
for var in "$@"
do
	allowed=0
	for opt in $OPTIONS
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

cd $DEST/$REPO
git checkout $BRANCH

git config --global user.name $USER
git config --global user.email $EMAIL
git config --global user.destination $DEST
git config --global user.backup $BACKUP
git config -l

read x

