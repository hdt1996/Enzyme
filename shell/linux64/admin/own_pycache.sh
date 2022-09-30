read -p "Drag/Drop or type in directory to chown: " loc
loc=$(echo $loc | sed s/\'//g)
find $loc -type d -iname "__pycache__" -exec sudo chown htran:htran {} \;

read -p "Done" x
