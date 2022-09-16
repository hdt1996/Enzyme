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
		read -p "
	NOTE:
	Target Branch: Should be branch to update
	Source Branch: Should be updated branch	
	
	Chosen "$id"	
	....Proceed with selection? [y/n/q]: " proceed
	echo
		if [ "$proceed" = "y" ]; then
			echo "$id"
			break
		elif [ "$proceed" = "q" ]; then
			echo 0
			break
		fi
	done
}


Process_Options(){ 
	echo
	read -p "	....Default or Interactive Mode? [d/i]" mode
	echo
	git checkout "$(echo $ch_id | sed -e 's/[\*\_]//g')"
	echo
	if [ "$mode" = "d" ]; then
		git rebase "$(echo $dst_id | sed -e 's/[\*\_]//g')"
		echo
		read -p "Push "$(echo $ch_id | sed -e 's/[\*\_]//g')" to Remote Repo? [y/n]: " to_push
		if [ "$to_push" = "y" ]; then
			$BASEDIR/push.sh
		fi
		echo
	elif [ "$mode" = "i" ]; then
		git rebase -i "$(echo $dst_id | sed -e 's/[\*\_]//g')"
		echo 
		read -p "Push "$(echo $ch_id | sed -e 's/[\*\_]//g')" to Remote Repo? [y/n]: " to_push
		if [ "$to_push" = "y" ]; then
			$BASEDIR/push.sh
		fi
		echo
	else
		echo "Returning to main menu"
	fi
}
BASEDIR=$(readlink -f $(dirname "$0"))
ORIG_BRANCH="$(git branch | grep '\* ' | sed -e 's/\* //')"
echo
read -p "
	..............Rebase Options..............
	menu: Create list of branches/commits to choose TARGET and SRC for rebase
	      NOTE: Using this will linearlize all newer branches (TODO PROMPT)
		      Be ready to handle rebase conflicts
		      If successful, new commits will need to be push (force?)
		      
	TODO-sync: Sync current branch to target branch (Handles 'n Commits Behind')
	      NOTE: ONLY do this after your Pull Requests are approved
	            Running this command with denied Pull Request without stashing
	            will cause you to LOSE YOUR WORK in working directory. Way to 
	            retrieve work is to checkout specific commit you pushed in PR

	continue: Continue existing rebase operation (if dealing with conflict)
	
	abort: Cancel existing rebase and restore commits to state prior
	.........................................
	Enter Rebase Option: " r_opt
if [ "$r_opt" = "continue" ]; then
	git rebase --continue
elif [ "$r_opt" = "abort" ]; then
	git rebase --abort
elif [ "$r_opt" = "menu" ]; then
	echo
	read -p "	Commit or Branch Mode [c/b]: " r_mode
	if [ "$r_mode" = "c" ]; then
		ch_id=$(MENU_PRE_SELECT "$(git log)" 'Target to Checkout' '^commit ' '' '([^\n]*\n){5}')
		if [ $ch_id = 0 ]; then
			echo "Going back to main menu"
			return
		fi
		dst_id=$(MENU_PRE_SELECT "$(git log)" 'Source to Rebase With' '^commit ' '' '([^\n]*\n){5}')
		if [ $dst_id = 0 ]; then
			echo "Going back to main menu"
			return
		fi
		Process_Options
	elif [ "$r_mode" = "b" ]; then
		ch_id=$(MENU_PRE_SELECT "$(git branch)" 'Target to Checkout' '' '' '')
		if [ $ch_id = 0 ]; then
			echo "Going back to main menu"
			return
		fi
		dst_id=$(MENU_PRE_SELECT "$(git branch)" 'Source to Rebase With' '' '' '')
		if [ $dst_id = 0 ]; then
			echo "Going back to main menu"
			return
		fi
		Process_Options	
	else
		echo "Returning to main menu"
	fi 
	
else
	echo "Going back to main menu"
fi












