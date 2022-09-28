echo

WHILE_INPUT(){
USER="$(git config user.name)"

PROMPT=1
while [ $PROMPT = 1 ] 
	do
		user="$USER"
		sm_repo=""
		sm_loc=""
		read -p "
		...................User Options......................
		<user>: Enter name of user that owns submodule repository
		<Enter>: Default to pulling from your account's repository
		<q>: Return to menu
		.......................................................
		Enter User Option: " user_opt
		if [ "$user_opt" = "q" ]; then
			break
		elif [ "$user_opt" = "" ]; then
			echo ""
			echo "\t\tSelected Current User: $user"
		else
			user="$user_opt"
		fi
		
		read -p "
		...................Choose Repo......................
		<repo>: Enter name of repository to include as submodule
		<Enter>: Back to User Selection
		.......................................................
		Enter Repo Name: " repo_opt
		
		if [ "$repo_opt" = "" ]; then
			continue
		else
			sm_repo="$repo_opt"
			echo ""
			echo "\t\tSelected Repo: $sm_repo"
		fi
		
		read -p "
		...................Choose Location......................
		<location>: Enter absolute path where submodule will be
		<Enter>: Back to User Selection
		.......................................................
		Enter Submodule Location: " loc_opt
		
		if [ "$loc_opt" = "" ]; then
			continue
		else
			sm_loc="$loc_opt"
			echo
			echo "\t\tSelected Location: $sm_loc"
		fi
		echo
		read -p "		Confirm? [y/n]: " conf
		echo
		if [ "$conf" = "y" ]; then
		
			git submodule add git@github.com:$user/$sm_repo.git $sm_loc || read -p "
			\r\t\tForce? This will overwrite ALL files in sub-repo directory [y/n] :" ovw
			if [ "$ovw" = "y" ]; then
				git submodule add --force git@github.com:$user/$sm_repo.git $sm_loc
			fi
			break
		
		fi

	done
}


read -p "
	...................Submodule Options......................
	add: Add new submodule by name
	<Enter>: Exit menu
	.......................................................
	Enter Branch Option: " r_opt
	
if [ "$r_opt" = "add" ]; then
	WHILE_INPUT
else
	echo "
	Returning to main menu..."
fi


return

for smf in $SUBMODULES
do
	loc=$(echo $smf | sed -e 's/[a-zA-Z0-9]\{1,\}\.sm\.sh//')
	custom_name=$(echo $smf | rev | cut -d '/' -f1 | rev | sed -e 's/\.sm\.sh//')
	sm_repo="$($smf)"
	echo
	echo "Removing Index -> $loc$custom_name"
	echo
	git rm -r --cached $loc$custom_name
	#rm -r $loc$sm_repo
	echo
	git submodule add git@github.com:$USER/$sm_repo.git $loc$custom_name || read -p "
	Force? This will overwrite ALL files in sub-repo directory [y/n] :" ovw
	if [ "$ovw" = "y" ]; then
		git submodule add --force git@github.com:$1/$sm_repo.git $loc$custom_name
	fi
	echo
done
