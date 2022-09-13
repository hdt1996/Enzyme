#!/bin/sh
N=0
CONCATENATE()
{
	i=0
	TABS=""
	while [ $i -lt $2 ]
	do
		i=$(($i+1))
		TABS="$TABS"'\t'
	done

	NEW_STR=""
	IFS=''
	I=0
	echo "$1" | while IFS= read -r line;
	do
		NEW_STR="$NEW_STR"'\n'"$TABS$line"
		echo "$NEW_STR"
		I=$(($I+1))

	done
}


RESULT="$(CONCATENATE $1 $2)"
echo "$NLines"
echo "$RESULT" | tail -n $(echo "$1" | wc -l)
