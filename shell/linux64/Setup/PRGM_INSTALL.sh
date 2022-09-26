#!/bin/sh
cd /home/htran/Desktop
find . -type f -iname "*.sh" -exec chmod +x {} \;

cd /home/htran/Desktop/Setup
find ./PRGM -type f -iname "*setup.sh" -exec {} \;
/home/htran/Desktop/Git/execs/run_git_config.sh
find ./PRGM -type f -regex '\.\/PRGM\/[a-zA-Z\_]+install[\_a-zA-Z]*\.sh' -exec {} \;

echo
echo "Completed Setup"
read x

