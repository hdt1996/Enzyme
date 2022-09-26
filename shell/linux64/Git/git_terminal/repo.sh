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
	add: Attach existing remote repository to current local repo
	
	NOTE: Delete is not an option for terminal actions.
	      You must go to github's website to delete via
	      'Danger Zone'...
	<Enter>: Exit menu
	.......................................................
	Enter Branch Option: " r_opt
	
if [ "$r_opt" = "add" ]; then
	read -p"	Enter name of new remote repo: " repo
	git remote add origin git@github.com:$(git config user.name)/$repo.git 
else
	echo
	echo "	Going back to main menu"
	break
fi
	done
















