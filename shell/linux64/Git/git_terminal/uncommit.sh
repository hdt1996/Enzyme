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
#				All 
MENU(){
	util="/home/htran/Desktop/SH_Utils/menu.sh"
	txt_src=$1
	title=$2
	search=$3
	replace=$4
	group_lines=$5
	get_detail(){
		rgx="$search$1$group_lines"
		echo "\t............................................"
		echo "\tChosen: $1"
		echo "..............Details................"
		echo "$5"
		echo "$txt_src" | pcregrep -M "$rgx"
		echo "....................................."
		echo "
	Options to Enter
	.........................................
	Y: Proceed to next step
	Q: Go back to select menu
	N/<Other>: Retry selection
	........................................."
		echo
		echo "\tContinue with your selection? : "
	}
	
	pending=0
	while [ $pending = 0 ]
	do
	
		id=$($util "$1" "$2" "$3" "$4")
		read -p "$(get_detail $id)" proceed
		if [ "$proceed" = "Y" ]; then
			echo "$id"
			break
		elif [ "$proceed" = "Q" ]; then
			echo 0
			break
		fi
	done
}


get_uc_type(){
	get_mrm(){
	read -rp "
	..............MENU RESET METHOD................

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
	if [ "$mrm" = "q" ]; then
		echo 0
	else
		echo "$mrm"
	fi
	}
	process_mrm(){
		if [ "$1" = "h" ]; then
			return 1
		elif [ "$1" = "q" ]; then
			return 1
		elif [ $1 = 0 ]; then
			:
		elif [ "$1" = "c" ]; then
			git revert "$2"
		elif [ "$1" = "cr" ]; then
		read x
		echo "$2"
		pre_commit="$2"'^1'
		GIT_SEQUENCE_EDITOR="sed -i -e s'/^pick $(echo $2 | cut -c1-7)/\ndrop $(echo $2 | cut -c1-7)/'" git rebase -i "$pre_commit"
		
		echo "BEFORE"
		git push origin main --force
		read x
		elif [ "$1" = "uc" ]; then
			git revert -n "$2"
		fi
		return 0
	}

	if [ "$2" = "menu" ]; then
		mrm="$(get_mrm)"
		process_mrm $mrm $1
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
	if [ "$uct" = "d" ]; then
		git reset --hard $1
	elif [ "$uct" = "p" ]; then
		git reset --soft $1
		echo
		echo "\tNo Options Selected: Going back to main menu"
	fi
	
	
}

choose_index(){
	opt_index=0
	for opt in $1
	do
		if [ $opt_index = $2 ]; then
			echo "$opt"
			break
		fi
		opt_index=$((opt_index+1))
	done
}
read -rp '
	..............UNCOMMIT MODE................

	Options to Enter
	.........................................
	last: Uncommit most recent commit
	menu: Choose commit to uncommit
	.........................................
	<Enter Option: ' choice

if [ "$choice" = "last" ]; then
	get_uc_type HEAD~1
	
elif [ "$choice" = "menu" ]; then

	id=$(MENU "$(git log)" 'Commit IDs' '^commit ' '' '([^\n]*\n){5}')
	if [ $id != 0 ]; then
		get_uc_type "$id" "$choice"
	fi
fi
echo










