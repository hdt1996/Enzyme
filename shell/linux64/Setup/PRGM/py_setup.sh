#!/bin/sh

sudo apt-get install python3.10 python3-pip
pip3.10 install numpy wheel packaging requests opt_einsum pandas matplotlib django
pip3.10 install keras_preprocessing --no-deps
