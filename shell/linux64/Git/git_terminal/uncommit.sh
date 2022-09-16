#!/bin/sh

#GIT COMMANDS
#	Rebase
#		Goal: Place current "checked out" branch ahead of ahead of "onto" branch
#		Process:
#			1) Find common ancestor between branches
#			2) Get diff between "checked out" branch and "onto" branch
#			3) Place diff commits after "onto" branch (merging to single)
#			4) Checked out branch should be to right of "onto" branch
#			5) If the result is a single linear line of commits 
#			   We can check out the "onto" branch and call merge
#				Head pointer simply moves -> AKA fast-forward
#

MENU_SELECT_DETAIL(){
	echo "\t............................................"
	echo "\tChosen: $1"
	echo "..............Details................"
	echo 
	echo "$2" | pcregrep -M "$3"
	echo
	echo "....................................."
	echo "
	Options to Enter
	.........................................
	y: Proceed to next step
	q: Go back to main menu
	<Other>: Retry selection
	........................................."
	echo
	echo "\tContinue with your selection? : "
}

MENU_PRE_SELECT(){
	util="/home/htran/Desktop/SH_Utils/menu.sh"
	txt_src="$1"
	title="$2"
	search="$3"
	replace="$4"
	group_lines="$5"
	pending=0
	while [ $pending = 0 ]
	do
	
		id=$($util "$txt_src" "$title" "$search" "$replace")
		rgx="$search$id$group_lines"
		read -p "$(MENU_SELECT_DETAIL "$id" "$txt_src" "$rgx")" proceed
		if [ "$proceed" = "y" ]; then
			echo "$id"
			break
		elif [ "$proceed" = "q" ]; then
			echo 0
			break
		fi
	done
}

MENU_POST_SELECT(){
	read -rp "
	..............UNCOMMIT TYPE................

	Options to Enter
	.........................................
	h - historical : Uncommit all branches after chosen branch (riskier) 
	c - commit: Creates new commit to reverse only chosen commit (safe)
	cr - commit rebase: Chosen commit's changes be wiped from history
			    Useful if chosen commit shows unauthorized data
	    IMPORTANT: Commits created after chosen commit will have their 
	    	       histories merged with newest revert commit. This will 
	    	       make these commits nonexistent while the changes from 
	    	       them persist. Potential risk is that one of the newer
	    	       commits being dependent on the one we are removing.
	    	       We can always use reflog to revert to previous version
	    	       of branch.
	     		    	       
	uc - uncommit: Reverses chosen commit but not does make new commit
		      Allows for more modifications after reverse to commit
	q - quit : Go back to main menu

	........................................
	<Enter Menu Reset Method : " mrm
	echo
	echo "....................."
	echo
	if [ "$mrm" = "h" ]; then
		return 1
	elif [ "$mrm" = "q" ]; then
		return 1
	elif [ "$mrm" = "c" ]; then
		git revert "$1"
	elif [ "$mrm" = "cr" ]; then
		pre_commit="$1"'^1'
		GIT_SEQUENCE_EDITOR="sed -i -e s'/^pick $(echo $1 | cut -c1-7)/\ndrop $(echo $1 | cut -c1-7)/'" git rebase -i "$pre_commit"
		git push origin "$ORIG_BRANCH" --force
	elif [ "$mrm" = "uc" ]; then
		git revert -n "$1"
	fi
	return 0
	
}

PROCESS_OPTIONS(){
	if [ "$2" = "menu" ]; then
		MENU_POST_SELECT "$1"
		proceed=$?
		if [ $proceed = 0 ]; then
			return 0
		fi 
	fi
	
	read -rp "
		..............CHANGE TYPE................

		Options to Enter
		.........................................
		d - discard : Remove vscode changes in work directory
		p - preserve : Uncommit while preserving changes in work directory
		<blank>: Go back to main menu
		.........................................
		<Enter Change Type : " uct	
	echo
	if [ "$uct" = "d" ]; then
		git reset --hard "$1"
		echo
		read -p "Push to Remote Repo? [y/n]: " to_push
		if [ "$to_push" = "y" ]; then
			$BASEDIR/push.sh
		fi
		echo
		
	elif [ "$uct" = "p" ]; then
		git reset --soft "$1"
		echo
		read -p "Push to Remote Repo? [y/n]: " to_push
		if [ "$to_push" = "y" ]; then
			$BASEDIR/push.sh
		fi
		echo
	else
		echo "\tNo Options Selected: Going back to main menu"
	fi
}
BASEDIR=$(readlink -f $(dirname "$0"))
ORIG_BRANCH="$(git branch | grep '\* ' | sed -e 's/\* //')"

read -rp '
	..............UNCOMMIT MODE................

	Options to Enter
	.........................................
	last: Uncommit most recent commit
	menu: Choose commit to uncommit
	.........................................
	<Enter Option: ' choice

if [ "$choice" = "last" ]; then
	PROCESS_OPTIONS HEAD~1
	
elif [ "$choice" = "menu" ]; then

	id=$(MENU_PRE_SELECT "$(git log)" 'Commit IDs' '^commit ' '' '([^\n]*\n){5}')
	if [ $id != 0 ]; then
		PROCESS_OPTIONS "$id" "$choice"
	fi
fi
echo










