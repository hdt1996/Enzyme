#!/bin/sh
read -rp "
	..............STAGE MODE................

	Options to Enter
	.........................................
	<filename> : Stage modified file by name
	all : Stage all modified in repository
	.........................................
	<Enter Option : " choice

if [ "$choice" = "all" ]; then
	git add --all
else
	git add $choice
fi
