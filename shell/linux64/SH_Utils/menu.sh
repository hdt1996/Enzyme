SHOW_DISPLAY()
{
	M_INDEX=0
	TEXT="$1"
	TITLE=$2
	SEARCH="$3"
	REPLACE='s/'"$3"'/'"$4"'/'


	LIST=$(echo "$TEXT" | grep -e "$SEARCH" | sed -e "$REPLACE")
	echo
	echo "\t..............MENU MODE............."
	echo
	echo "\t..............$TITLE................"
	for opt in $LIST
	do
		echo "\t$M_INDEX $opt"
		M_INDEX=$((M_INDEX+1))
	done
	echo ""
	echo "\tSpecify item index for $2: "
}

CHOOSE_INDEX(){
	opt_index=0
	list=$(echo "$1" | grep -E '[\t]*[0-9]{1,} ' | sed -e 's/[\t]*[0-9]\{1,\} //')
	for opt in $list
	do
		if [ $opt_index = $2 ]; then
			echo "$opt"
			break
		fi
		opt_index=$((opt_index+1))
	done
}
	
DISPLAY=$(SHOW_DISPLAY "$1" "$2" "$3" "$4")

read -p "$DISPLAY" SELECTED
SELECTED_ID="$(CHOOSE_INDEX "$DISPLAY" "$SELECTED")"
echo "$SELECTED_ID"





