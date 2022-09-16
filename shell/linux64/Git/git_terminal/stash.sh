#!/bin/sh

#GIT COMMANDS
#	Stash
#		Goal: Backup all changes made in working directory before removing them
#		Usages: 
#			git stash for stashing
#			git stash -m <name> for stashing with title
#				Eqivalent: git stash push -m <name>
#			git stash apply <number> to re-input changes to working directory
#			git stash list for showing all stashes by list
#			git stash clear for removing all stashes
#			git stash drop <num> for removing specific stash
#			git stash pop <num> for applying and removing specific stash
	
	
MENU_SELECT_DETAIL(){
	echo "\t............................................"
	echo "\tChosen: $1"
	read -p "
		Detail Options
		.........................................
		<filename>: Show diffs for specific file
		all: Show all diffs (May be large echo output)
		.........................................
		Enter Option: " d_opt
	
	echo "..............Details................"
	echo 
	if [ "$d_opt" = "all" ]; then
		git show stash"$1"
	else
		git show stash"$1:$d_opt"
	fi
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
	
		id=$($util "$1" "$2" "$3" "$4")
		id="$(echo $id | sed -e 's/:.*//')"
		read -p "$(MENU_SELECT_DETAIL $id)" proceed
		if [ "$proceed" = "y" ]; then
			echo "$id"
			break
		elif [ "$proceed" = "q" ]; then
			echo 0
			break
		fi
	done
}


PROCESS_OPTIONS(){
	read -rp "

	Current Stash Options
	.........................................
	apply: Apply current stash
	apply p: Apply current stash and remove from stash list
	
	drop: Delete current stash
	........................................
	<Enter Menu Reset Method : " opt
	echo
	if [ "$opt" = "apply" ]; then
		git stash apply stash"$id"
	elif [ "$opt" = "apply p" ]; then
		git stash pop stash"$id"
	elif [ "$opt" = "drop" ]; then
		git stash drop stash"$id"
	fi
	echo
}


read -rp '
	..............BACKUP MODE................

	Options to Enter
	.........................................
	add: Make new stash from all current changes - default WIP title
	add c: Make new stage from all current changes - custom name for title
	
	apply: Apply most recent stash
	apply p: Apply most recent stash and remove it from stash list
	
	clear: Remove all stashes
	
	menu: List all stashes and choose one for operation
	      Use for finding non-recent stash to operate
	.........................................
	<Enter Option: ' choice
echo
if [ "$choice" = "add" ]; then
	git stash
elif [ "$choice" = "add c" ]; then
	read -p "	Enter custom name: " custom_name
	echo
	git stash -m "$custom_name"
elif [ "$choice" = "apply" ]; then
	git stash apply
elif [ "$choice" = "apply p" ]; then
	git stash pop
elif [ "$choice" = "clear" ]; then
	git stash clear
elif [ "$choice" = "menu" ]; then
	id=$(MENU_PRE_SELECT "$(git stash list)" 'Stash IDs' '^stash' '' '')
	if [ $id != 0 ]; then
		PROCESS_OPTIONS "$id"
	fi
else
	:
fi
echo








