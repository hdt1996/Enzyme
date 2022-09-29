read -p "Drag/Drop or type in directory to chmod: " loc
loc=$(echo $loc | sed s/\'//g)
find $loc -type f -iname "*.sh" -exec sudo chmod +x {} \;
