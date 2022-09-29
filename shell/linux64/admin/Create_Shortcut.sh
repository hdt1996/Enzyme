cd ~/Desktop

read -p \
"What icon do you want?
.......................
1) git
2) standard
......................
Enter name: " icon

case "$icon" in
	"git")
	icon=$(readlink -f ./admin/src/git.png);;
	"standard")
	icon=$(readlink -f ./admin/src/exec_icon.jpg);;
esac

read -p "Drag/Drop or Write your scripts path here: " inps
for inp in $inps
do
	inp=$(echo $inp | sed s/\'//g)
	custom_name="$(echo $inp | rev | cut -d '/' -f1 | rev | sed -e 's/\.sh//')"
	echo \
"
[Desktop Entry]
Version=1.0
Exec=$inp
Name=$custom_name
GenericName=$custom_name
Comment=$custom_name
Encoding=UTF-8
Terminal=true
Type=Application
Icon="$icon"
Categories=Application;Network;TEST
" > ./$custom_name.desktop
	sudo chown htran:htran ./$custom_name.desktop 
	sudo chmod ug+x ./$custom_name.desktop 
	gio set ./$custom_name.desktop metadata::trusted true
done



