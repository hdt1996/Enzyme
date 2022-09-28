
sudo apt-get install resolvconf
sudo systemctl status resolvconf.service
sudo nano /etc/resolvconf/resolv.conf.d/head
sudo systemctl restart resolvconf.service
sudo systemctl restart systemd-resolved.service
read -p "Ready to reboot? [y/n]: " proceed
if [ "$proceed" = "y" ]; then
	:
else
	echo "Not rebooting for now"
	return 
fi
sudo reboot
