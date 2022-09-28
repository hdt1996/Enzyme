#!/bin/sh

sudo apt-get update && time sudo apt-get dist-upgrade
sudo add-apt-repository universe
sudo apt-get install unzip dpkg git imagemagick #gnome-shell-extensions gnome-tweaks

#################################################### DOCKER #############################################################
sudo apt-get install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose



sudo groupadd docker
sudo gpasswd --add $USER docker


#sudo curl "https://desktop.docker.com/linux/main/amd64/docker-desktop-4.12.0-amd64.deb" -o "/tmp/docker-desktop-4.12.0-amd64.deb"
#sudo apt-get install /tmp/docker-desktop-4.12.0-amd64.deb

##################################################### AWS ############################################################
sudo curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip"
sudo unzip /tmp/awscliv2.zip
sudo /tmp/aws/install
sudo curl -L https://raw.githubusercontent.com/docker/compose-cli/main/scripts/install/install_linux.sh | sh #AWS INTEGR WITH DOCKER COMPOSE
sudo curl "https://s3.amazonaws.com/session-manager-downloads/plugin/latest/ubuntu_64bit/session-manager-plugin.deb" -o "/tmp/session-manager-plugin.deb"
sudo apt-get install /tmp/session-manager-plugin.deb
#############################################################################################################################
#-------------------- Using resolvconf for DNS servers (Not going to use anymore) ---------
#sudo apt-get install resolvconf
#sudo systemctl status resolvconf.service
#sudo nano /etc/resolvconf/resolv.conf.d/head
#sudo systemctl restart resolvconf.service
#sudo systemctl restart systemd-resolved.service

##################################################### Minimalistic way of setting DNS Servers (Preferred) ####################
sudo rm /etc/resolv.conf #Remove original with symlink and systemd permissions
sudo cp ./configs/resolv.conf /etc/resolv.conf

sudo apt-get update && time sudo apt-get dist-upgrade

