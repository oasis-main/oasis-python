#!/bin/sh -e

echo "TLS Request Encryption (HTTPS only...)"
sudo snap install --classic certbot
sudo certbot --nginx -d demo.oasis-x.io -d www.demo.oasis-x.io
sudo cp /home/ubuntu/oasis-python/configs/oasis_python_secure.nginx /etc/nginx/sites-available/demo.oasis-x.io
sudo systemctl reload nginx
sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'

echo "Restartign Nginx"
sudo systemctl restart nginx