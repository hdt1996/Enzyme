#!/bin/sh
cd /home/htran/Desktop
echo "$PWD"
find . -type f -iname "*.sh" -exec chmod +x {} \;
cd /home/htran/Desktop/Setup
find ./Linux -type f -iname "*.sh" -exec echo -e "\n\nFound {}\n\nExecuting...\n" \; -exec {} \;
find ./PRGM -type f -iname "*setup.sh" -exec echo -e "\n\nFound {}\n\nExecuting...\n" \; -exec {} \;
find ./PRGM -type f -regex '\.\/PRGM\/[a-zA-Z\_]+install[\_a-zA-Z]*\.sh' -exec echo -e "\n\nFound {}\n\nExecuting...\n" \; -exec {} \;
echo "Completed Setup"
read x

