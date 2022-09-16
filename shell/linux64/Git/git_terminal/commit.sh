#!/bin/sh
read -rp '
	..............COMMIT MODE................

	Options to Enter
	.........................................
	<Commit MSG> : Message of your commit
	.........................................
	<Enter Commit MSG : ' choice
echo
git commit -m "$choice"
echo
