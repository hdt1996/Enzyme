#!/bin/sh
sudo apt-get install apt-transport-https curl gnupg
curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor >bazel-archive-keyring.gpg
sudo mv bazel-archive-keyring.gpg /usr/share/keyrings
arch=$(dpkg --print-architecture)
echo "deb [arch=$arch signed-by=/usr/share/keyrings/bazel-archive-keyring.gpg] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
sudo apt-get update && sudo apt-get install bazel
sudo apt-get update && sudo apt full-upgrade
echo "Done with Bazel Setup"

tf_dest=$(/home/htran/Desktop/Git/git_clone.sh -repo tensorflow -user tensorflow | tail -n 1)
cd $tf_dest && bazel build --jobs=10 --local_ram_resources="HOST_RAM*.65" //tensorflow/tools/pip_package:build_pip_package
./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
sudo mv /tmp/tensorflow_pkg/tensorflow*.whl /tmp/tensorflow_pkg/tensorflow_linux.whl 
pip3.10 install /tmp/tensorflow_pkg/tensorflow_linux.whl
pip3.10 install tensorflow_probability 

