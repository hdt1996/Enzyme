#!/bin/sh
sudo apt update
sudo apt upgrade
sudo add-apt-repository universe
wget https://release.gitkraken.com/linux/gitkraken-amd64.deb
sudo dpkg -i gitkraken-amd64.deb
sudo apt-get install unzip dpkg git gnome-shell-extensions gnome-tweaks git

