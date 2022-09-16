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
		if [ "$id" = "" ]; then
			echo
			break
		fi
		
		read -p "
	You have chosen: --> $id
		
	....Proceed with selection? [y/n/q]: " proceed
		if [ "$proceed" = "y" ]; then
			echo "$id"
			break
		elif [ "$proceed" = "q" ]; then
			echo 0
			break
		fi
	done
}

ERROR_HANDLING(){
	if [ "$1" = "del" ]; then 
		echo
		read -p "	Force Delete? [y/n]: " to_force
		echo
		if [ "$to_force" = "y" ]; then
			git branch -D "$2"
		else
			echo "	No Delete Occurred. Exiting..."
		fi
	fi
}

Process_Options(){ 
	echo
	if [ "$1" = "" ]; then
		echo "	....No ID Selected: Returning to main menu"
		return
	fi
	target_branch="$(echo $1 | sed -e 's/[\*\_]//g' | sed -e 's/origin\///')"
	if [ "$2" = "ckout" ]; then
		git checkout "$target_branch"
	elif [ "$2" = "del l" ]; then
		git branch --delete "$target_branch" || ERROR_HANDLING "del" "$target_branch"
	elif [ "$2" = "del r" ]; then
		git push origin -d "$target_branch"
		git remote prune origin
	elif [ "$2" = "arch cl" ]; then
		git tag archive/commits/"$target_branch" "$target_branch"
		echo "
		...Archived commit. Delete only possible with rebase"
	elif [ "$2" = "arch cr" ]; then
		git tag archive/commits/"$target_branch" "$target_branch"
		echo "
		...Archived commit. Delete only possible with rebase"
	elif [ "$2" = "arch bl" ]; then
		git tag archive/commits/"$target_branch" "$target_branch"
		git branch --delete "$target_branch" || ERROR_HANDLING "del" "$target_branch"
	elif [ "$2" = "arch br" ]; then #REMOTE ARCHIVE CURRENTLY NOT OFFERED BY GITHUB. USE/MAKE OTHER SERVICE
		git tag archive/commits/"$target_branch" "$target_branch"
		git branch --delete "$target_branch" || ERROR_HANDLING "del" "$target_branch"
		git push origin -d "$target_branch"
	elif [ "$2" = "ovwr" ]; then
		echo
		read -rp "
		..............OVERWRITE TYPE................

		Options to Enter
		.........................................
		d - discard : Remove changes in work directory
		p - preserve : Uncommit while preserving changes in work directory
		<blank>: Go back to main menu
		.........................................
		<Enter Change Type : " uct	
		echo
		if [ "$uct" = "d" ]; then
			git reset --hard "$target_branch"
			echo
			read -p "	Push to Remote Repo? [y/n]: " to_push
			if [ "$to_push" = "y" ]; then
				$BASEDIR/push.sh
			fi
			echo
			
		elif [ "$uct" = "p" ]; then
			git reset --soft "$target_branch"
			echo
			read -p "	Push to Remote Repo? [y/n]: " to_push
			if [ "$to_push" = "y" ]; then
				$BASEDIR/push.sh
			fi
			echo
		else
			echo "\tNo Options Selected: Going back to main menu"
		fi
	fi
	echo
}

MENU_SOURCE_TYPE(){
	if [ "$1" = "l" ]; then
		echo "$(git branch)"
	elif [ "$1" = "r" ]; then
		echo "$(git branch -r)"
	else
		echo "$(git branch)"
	fi
}



echo
PROMPT=1
while [ $PROMPT = 1 ] 
	do
BASEDIR=$(readlink -f $(dirname "$0"))
ORIG_BRANCH="$(git branch | grep '\* ' | sed -e 's/\* //')"
read -p "
	...................Branch Options......................
	show: Show all branches
	show l: Show Local Branches
	show r: Show Remote Branches
	
	add l: Make new local branch and switch/checkout to it
	add ln: Make new local branch without switching/checkout
	add r: Make new remote branch and switch/checkout to it
	add rn: Make new remote branch and go back to original

	ckout: Check out branch by name
	ckout li: Check out branch from list menu selection
	
	arch: Archive branch by name (If not already by PR Appr)
	      Note: This will delete the local or (and remote branch)
	      To Re-Access: 1) git checkout -b <name> archive/<name>
	      		    2) Go to Pull Request -> Restore branch
	arch li: Archive branch chosen in list menu selection
	
	del: Delete branch by name
	del li: Delete branch from list menu selection
	
	ovwr: Overwrite existing branch with specified commit/branch
	ovwr li: Overwrite existing branch with selection from menu
	
	<Enter>: Exit menu
	.......................................................
	Enter Branch Option: " r_opt

if [ "$r_opt" = "show" ]; then
	git branch -a
	read p
elif [ "$r_opt" = "show l" ]; then
	git branch
	read p
elif [ "$r_opt" = "show r" ]; then
	git branch -r
	read p
##########################################################################################################
elif [ "$r_opt" = "add r" ]; then
	read -p "	Enter name of new branch: " new_name
	echo
	git checkout -b "$new_name"
	git push -u origin "$new_name"
	echo
	echo "....Checked out and pushed $new_name to remote origin"
elif [ "$r_opt" = "add rn" ]; then
	read -p "	Enter name of new branch: " new_name
	echo
	git checkout -b "$new_name"
	git push -u origin "$new_name"
	git checkout "$ORIG_BRANCH"
	echo
	echo "....Made new remote branch and returned to $ORIG_BRANCH"
elif [ "$r_opt" = "add l" ]; then
	read -p "	Enter name of new branch: " new_name
	echo
	git checkout -b "$new_name"
	echo
	echo "....Checked out $new_name locally -> No change to remote"
elif [ "$r_opt" = "add ln" ]; then
	read -p "	Enter name of new branch: " new_name
	echo
	git branch "$new_name"
##########################################################################################################
elif [ "$r_opt" = "del" ]; then
	echo
	read -p "	Continue? [y/n]: " r_mode
	echo
	read -p "	Enter name of branch to delete: " name
	echo
	if [ "$r_mode" = "y" ]; then
		read -p "	Local or Remote Source [l/r]: " r_source 
		Process_Options	"$name" "del $r_source"
	else
		echo "Returning to main menu"
	fi 
elif [ "$r_opt" = "del li" ]; then
	echo
	read -p "	Continue? [y/n]: " r_mode
	echo
	if [ "$r_mode" = "y" ]; then
		read -p "	Local or Remote Source [l/r]: " r_source 
		ch_id=$(MENU_PRE_SELECT "$(MENU_SOURCE_TYPE $r_source)" 'Branch to Delete' '' '' '')
		Process_Options	"$ch_id" "del $r_source"
	else
		echo "Returning to main menu"
	fi 
##########################################################################################################
elif [ "$r_opt" = "arch" ]; then
	echo
	read -p "	Select branch by Commit ID or Branch [c/b]: " r_mode
	read -p "	Enter name/id of branch/commit: " name
	if [ "$r_mode" = "c" ]; then
		read -p "	Local or Remote Source [l/r]: " r_source 
		Process_Options	"$name" "arch $r_mode$r_source"
		
	elif [ "$r_mode" = "b" ]; then
		read -p "	Local or Remote Source [l/r]: " r_source 
		Process_Options	"$name" "arch $r_mode$r_source"
	else
		echo "Returning to main menu"
	fi 
	
elif [ "$r_opt" = "arch li" ]; then
	echo
	read -p "	Select branch by Commit ID or Name [c/b]: " r_mode
	if [ "$r_mode" = "c" ]; then
		read -p "	Local or Remote Source [l/r]: " r_source 
		ch_id=$(MENU_PRE_SELECT "$(git log)" 'Commit to Checkout' '^commit ' '' '([^\n]*\n){5}')
		Process_Options	"$ch_id" "arch $r_mode$r_source"
		
	elif [ "$r_mode" = "b" ]; then
		read -p "	Local or Remote Source [l/r]: " r_source 
		ch_id=$(MENU_PRE_SELECT "$(MENU_SOURCE_TYPE $r_source)" 'Branch to Checkout' '' '' '')
		Process_Options	"$ch_id" "arch $r_mode$r_source"
	else
		echo "Returning to main menu"
	fi 
##########################################################################################################
elif [ "$r_opt" = "ckout" ]; then
	read -p "	Enter name/id of branch/commit: " name
	echo
	git checkout "$name"
	echo
	
elif [ "$r_opt" = "ckout li" ]; then
	echo
	read -p "	Select by Commit ID or Branch Name [c/b]: " r_mode
	if [ "$r_mode" = "c" ]; then
		ch_id=$(MENU_PRE_SELECT "$(git log)" 'Commit to Checkout' '^commit ' '' '([^\n]*\n){5}')
		Process_Options "$ch_id" 'ckout'
	elif [ "$r_mode" = "b" ]; then
		read -p "	Local or Remote Source [l/r]: " r_source 
		ch_id=$(MENU_PRE_SELECT "$(MENU_SOURCE_TYPE $r_source)" 'Branch to Checkout' '' '' '')
		Process_Options	"$ch_id" 'ckout'
	else
		echo "Returning to main menu"
	fi 
##########################################################################################################
elif [ "$r_opt" = "ovwr" ]; then
	echo
	read -p "	Enter name/id of source branch/commit: " name
	echo
	echo "	Chosen as source for overwrite: $name"
	echo
	read -p "	Continue? [y/n]: " r_mode
	if [ "$r_mode" = "y" ]; then
		Process_Options "$name" 'ovwr'
	else
		echo "	...Going back to main menu"
	fi
	
elif [ "$r_opt" = "ovwr li" ]; then
	echo
	read -p "	Commit or Branch Mode [c/b]: " r_mode
	
	if [ "$r_mode" = "c" ]; then
		ch_id=$(MENU_PRE_SELECT "$(git log)" 'Source of Overwrite' '^commit ' '' '([^\n]*\n){5}')
		if [ $ch_id = 0 ]; then
			echo "Going back to main menu"
			return
		fi
		Process_Options "$ch_id" 'ovwr'
	elif [ "$r_mode" = "b" ]; then
		ch_id=$(MENU_PRE_SELECT "$(MENU_SOURCE_TYPE $r_source)" 'Source of Overwrite' '' '' '')
		if [ $ch_id = 0 ]; then
			echo "Going back to main menu"
			return
		fi
		Process_Options "$ch_id" 'ovwr'
	
	else
		echo "	...Going back to main menu"
	fi
	
	
else
	echo
	echo "	Going back to main menu"
	break
fi
	done
















