#!/bin/sh
read -rp '
	..............UNSTAGE MODE................

	Options to Enter
	.........................................
	<filename> : Unstage modified file by name
	all : Unstage all modified in repository
	.........................................
	<Enter Option : ' choice
echo
if [ "$choice" = "all" ]; then
	#git checkout -- . DEPRECATED
	git restore --staged .
else
	#git checkout -- $choice DEPRECATED
	git restore --staged "$choice"
fi
echo 
echo "Success --- Unstaged $choice "
