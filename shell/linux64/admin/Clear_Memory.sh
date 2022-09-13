#!/bin/sh
echo 1 >  /proc/sys/vm/drop_caches
echo 2 >  /proc/sys/vm/drop_caches
sudo echo 3 >  /proc/sys/vm/drop_caches
sudo swapoff -a
sudo swapon -a
free -h
