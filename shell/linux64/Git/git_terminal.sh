#!/bin/sh
#var OPTIONS -- Add Named Arguments Separated by Space
#Declare global vars after OPTIONS for use in executed command (Last Line)
#	Ex. USER=""
#	Ex. --CATEGORY=""   NOTE THE -- double hyphens included in argument!
#VARS_ASSIGN Function: 
#	Each case is specified per each named arguments (opt) in OPTIONS
#		Ex. USER) ...execution
#		Ex. --CATEGORY) ...execution
#	Execution of case: Update related global variable to $2
#		Ex. USER=$2
#ARG_BOOL Function:
#	Function to handle passing non-kwarg/single arg that executables need for true/false
#	ARGS
#		$1: Value arg passed in script: true or false | 0 or 1
#		$2: Dependency arg required for dependency executable i.e. -o -p -a etc.
#KWARG Function:
#	Function to handle passing kwargs that executables need
#	ARGS
#		$1: Dependency arg required for dependency executable i.e. -password or -p
#		$2: Value arg passed in script: string or number
#	Result should look like -password MyCustomPassword or -p MyCustomPassword
#KWARG_KEYEQVAL Function:
#	Function to handle passing kwargs where value is key=value pair
#	ARGS
#		$3: Dependency arg required for dependency executable i.e. -password or -p
#		$1: Key arg from K=V pair (Named arg passed in script)
#		$2: Value arg from K=V pair (Value arg passed in script)
#Join Commands:
#	&& execute following after success of previous
#	& execute previous in background and following no matter result of previous
#	| execute previous and use output(stdout/echo) as input to following (auto-prompt)
#	|| execute following only if previous failed (returns nonzero code; zero = success)
#General Commands:
#	sed -e 's/[to_find]/[replacer]/[global]' source_string
#		NOTE:
#			sed automatically removes and reinserts newline. So \n does not work
#	grep -e '[regex]' source_string
#		NOTE:	
#			like sed NOTE above
#	tr -d [delimiter] source_string
#		NOTE: FOR DELETING ONLY
#	Quotes
#		Apostrophe means no variables to evaluate
#		Double Quotes means we have variables to evaluate (format string)
#	Escaping
#		To escape "\n" in echo we need at least three
#		To escape '\n' in echo we need at least 2
BASEDIR=$(readlink -f $(dirname $0))
OPTIONS="-repo -user -branch"
BRANCH=""
REPO=""
USER="$(git config user.name)"
DEST="$(git config user.destination)"


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
	case "$1" in
	"-repo")
		REPO="$2";;
	"-user")
		USER="$2";;
	"-branch")
		BRANCH="$2";;
	esac
}

INPUT_ASSIGN(){
	case "$1" in
	
	"submodule")
		$BASEDIR/git_terminal/submodule.sh;;
	"autopull")
		echo
		read -p "Auto-Pull for this $REPO and submodules? [y/n]: " setauto;;
	"retrack")
		git rm -r --cached . > /dev/null 2>&1
		read -p "Stage all? [y/n] :" p
		if [ "$p" = "n" ]; then
			:
		else
			git add --all
			git restore --staged .
		fi
		;;
	"cmd")
		read -rp "Enter your custom command: " custom_cmd
		echo
		$custom_cmd
		echo
		read -p "Press Enter to continue: " p;;
	"repo")
		$BASEDIR/git_terminal/repo.sh;;
	"branch")
		$BASEDIR/git_terminal/branch.sh;;
	"merge")
		$BASEDIR/git_terminal/merge.sh;;
	"rebase")
		$BASEDIR/git_terminal/rebase.sh;;
	"stage")
		$BASEDIR/git_terminal/stage.sh;;
		
	"unstage")
		$BASEDIR/git_terminal/unstage.sh;;
	"commit")
		$BASEDIR/git_terminal/commit.sh;;
	"uncommit")
		$BASEDIR/git_terminal/uncommit.sh;;
	"push")
		$BASEDIR/git_terminal/push.sh;;
	"backup")
		$BASEDIR/git_terminal/stash.sh;;
	"log")
		echo "q" | git --no-pager log
		read x;;
	"reflog")
		echo "q" | git --no-pager reflog
		read x;;
	esac
	echo
}

setauto=""
WHILE_INPUT(){
PROMPT=1
while [ $PROMPT = 1 ] 
	do
		echo
		if [ "$setauto" = "y" ]; then
			git pull > /dev/null 2>&1
			git submodule update --recursive --remote > /dev/null 2>&1
			echo
			echo '\rCompleted fetch and pull...'
		fi
		echo "--------------------------------------------------------"
		git status
		echo "--------------------------------------------------------"
		INPUT_I=1

		current_branch="$(git branch -a | grep '\* ' | sed -e 's/\* //')"
		echo "Repo: $REPO" 
		if [ "$current_branch" = "" ]; then
			echo "Created Local Branch: dev"
		else
			echo "Current Branch: $current_branch"
		fi
		
		echo "............................"
		echo "Choose one of the following:"
		for opt in $1
		do
			echo "$INPUT_I) $opt"
			INPUT_I=$((INPUT_I+1))
		done
		echo "............................"
		read -p "Enter Action : " action

		if [ "$action" = "quit" ]; then
			break
		fi
		INPUT_ASSIGN "$action"
		echo "________________________________________________________"
	done
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
		VARS_ASSIGN "$CURR_VAR" "$var"
		INDEX=0
	else
		INDEX=$((INDEX+1))
	fi
	
done

cd "$DEST/$REPO"
git checkout -b "$BRANCH" > /dev/null 2>&1
echo
WHILE_INPUT "autopull submodule retrack cmd repo branch merge rebase stage unstage commit uncommit push backup log reflog quit"
read x

