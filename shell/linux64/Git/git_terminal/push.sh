ORIG_BRANCH="$(git branch | grep '\* ' | sed -e 's/\* //')"
HANDLE_ERROR(){
	echo
	read -p "
	Create upstream remote? [y/n]: " to_create
	echo
	if [ "$to_create" ]; then
		git push --set-upstream origin $1
	fi
}

read -p "	
	Push Target Options
	.......................................................
	<enter/blank> - default: Use current branch's remote location
	<name>: Push commits to different target branch
	
	q - quit: Back to main menu
	.......................................................
	Enter Push Location: [d/<name>]: " p_target
echo
if [ "$p_target" = "" ]; then
	p_target="$ORIG_BRANCH"
	
elif [ "$p_target" = "q" ]; then
	echo "	Returning to main menu"
	return
fi
echo
read -p "	Force? [y/n]: " force
echo
if [ "$force" = "y" ]; then
 	git push origin --force $ORIG_BRANCH:$p_target || HANDLE_ERROR $ORIG_BRANCH:$p_target
elif [ "$force" = "n" ]; then
	git push origin $ORIG_BRANCH:$p_target || HANDLE_ERROR $ORIG_BRANCH:$p_target
else
	echo "	Canceled"
fi
