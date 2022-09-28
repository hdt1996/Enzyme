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

echo "clone git@github.com:$USER/$REPO.git"
git clone git@github.com:$USER/$REPO.git "$DEST/$REPO"

#SCAN FOR SUBMODULES
cd "$DEST/$REPO"
SUBMODULES="$(find . -type f -iname "*.sm.sh")"
for smf in $SUBMODULES
do
	loc=$(echo $smf | sed -e 's/[a-zA-Z0-9]\{1,\}\.sm\.sh//')
	custom_name=$(echo $smf | rev | cut -d '/' -f1 | rev | sed -e 's/\.sm\.sh//')
	echo $custom_name
	read x
	sm_repo="$($smf)"
	echo
	echo "Removing Index -> $loc$custom_name"
	echo
	git rm -r --cached $loc$custom_name
	#rm -r $loc$sm_repo
	echo
	git submodule add git@github.com:$USER/$sm_repo.git $loc$custom_name ||\
	echo && read -p "Force? This will overwrite ALL files in sub-repo directory [y/n] :" ovw
	if [ "$ovw" = "y" ]; then
		git submodule add --force git@github.com:$USER/$sm_repo.git $loc$custom_name
	fi
	echo
done

