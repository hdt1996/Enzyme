#!/bin/sh

OPTIONS="-repo -user"
REPO=""
USER="$(git config user.name)"
DEST="$(git config user.destination)"
echo "$DEST"
CASE_ASSIGN(){
	case "$1" in
	"-repo")
		REPO="$2";;
	"-user")
		USER="$2";;
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
		CASE_ASSIGN "$CURR_VAR" "$var"
		INDEX=$((0))
	else
		INDEX=$((INDEX+1))
	fi
	
done
BASEDIR=$(readlink -f $(dirname $0))
echo "clone git@github.com:$USER/$REPO.git"
git clone git@github.com:$USER/$REPO.git "$DEST/$REPO"

#SCAN FOR SUBMODULES
cd "$DEST/$REPO"
git submodule update --init --recursive
#$BASEDIR/git_terminal/submodules.sh "$USER"

