#Pass directory or file with regex as argument
find $1 -type f -iname "*.sh" -exec chmod +x {} \;
