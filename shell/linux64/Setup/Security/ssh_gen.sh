#!/bin/bash
DATE="$(date '+%m%d%Y_%X' | sed -e 's/AM//' -e 's/PM//' -e 's/ //g' -e 's/://g')"
read -p "Please enter new name for SSH files: " filename
echo
cd ~/.ssh
mkdir ./keys
echo "./keys/$filename$DATE" | ssh-keygen
ssh-add "./keys/$filename$DATE"
echo
echo "Generated public key and installed private key!"
echo
read -p "Please assign public key to your git platform" p

