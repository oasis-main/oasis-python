#!/bin/sh -e

echo "Installing Nginx"
sudo apt-get install nginx -y


echo "Configuring Nginx Default"
sudo ufw allow 'Nginx HTTP'
sudo cp /home/ubuntu/oasis-python/configs/oasis_python_conf_setup.nginx /etc/nginx/sites-available/demo.oasis-x.io 
sudo ln -s /etc/nginx/sites-available/demo.oasis-x.io /etc/nginx/sites-enabled/ 
sudo cp /home/ubuntu/oasis-python/configs/oasis_python_global.nginx /etc/nginx/nginx.conf 

echo "Restarting Nginx"
sudo systemctl restart nginx
