#!/bin/sh

#GIT COMMANDS
#	Rebase --onto
#		Goal: Place current "checked out" branch ahead of ahead of "onto" branch
#		Process:
#			1) Find common ancestor between branches
#			2) Get diff between "checked out" branch and "onto" branch
#			3) Place diff commits after "onto" branch (merging to single)
#			4) Checked out branch should be to right of "onto" branch
#			5) If the result is a single linear line of commits 
#			   We can check out the "onto" branch and call merge
#				Head pointer simply moves -> AKA fast-forward
#	git checkout <target>
#	Rebase <source>
#		Goal: Place current "checked out" branch ahead of ahead of "onto" branch
#		Process:
#			1) Find common ancestor between both branches
#			2) Get diff between checked out branch and source branch
#			3) Add diffs onto checked out branch in linear fashion
#			4) Push changes and head pointer will fast-forward if no conflict
#	git checkout <target>
#	git merge <source>
#		Goal: Create commit that combines checked out branch and source branch
#		      at common ancester AKA where the two branches diverged
#		Nondestructive: No commit histories modified or destroyed
#		Process:
#			1) Combine all commits from source branch into one commit
#			2) Push commit onto checked-out branch
#			3) Branches will still be attached to commit history
#			4) git nodes will show one source branch pulled" into target
#			NOTE: git pull always does a merge 
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
	read -p "	Continue? [y/n]: " proceed
	echo
	git checkout "$(echo $ch_id | sed -e 's/[\*\_]//g')"
	echo
	if [ "$proceed" = "y" ]; then
		git merge "$(echo $dst_id | sed -e 's/[\*\_]//g')"
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
	..............Merge Options..............
	menu: Create list of branches/commits to choose TARGET and SRC for merge
	      NOTE: Creates 

	continue: Continue existing merge operation (if dealing with conflict)
	
	abort: Cancel existing merge and restore commits to state prior
	.........................................
	Enter Merge Option: " r_opt
if [ "$r_opt" = "continue" ]; then
	git merge --continue
elif [ "$r_opt" = "abort" ]; then
	git merge --abort
elif [ "$r_opt" = "menu" ]; then
	echo
	read -p "	Commit or Branch Mode [c/b]: " r_mode
	if [ "$r_mode" = "c" ]; then
		ch_id=$(MENU_PRE_SELECT "$(git log)" 'Target to Checkout' '^commit ' '' '([^\n]*\n){5}')
		if [ $ch_id = 0 ]; then
			echo "Going back to main menu"
			return
		fi
		dst_id=$(MENU_PRE_SELECT "$(git log)" 'Source to Merge With' '^commit ' '' '([^\n]*\n){5}')
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
		dst_id=$(MENU_PRE_SELECT "$(git branch)" 'Source to Merge With' '' '' '')
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












