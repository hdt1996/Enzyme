#!/bin/sh
#sudo apt-get install default-jre default-jdk
sudo wget https://download.oracle.com/java/19/latest/jdk-19_linux-x64_bin.deb -O /tmp/jdk-19_linux-x64_bin.deb
sudo apt-get install /tmp/jdk-19_linux-x64_bin.deb
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-19/bin/java 1919
read -p "Done" x
