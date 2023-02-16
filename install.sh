echo "Installing uvicorn"
sudo apt-get install uvicorn -y #FastAPI Runtime
echo "Installing python3-pip"
sudo apt-get install python3-pip -y
echo "Installing python3-venv"
sudo apt-get install python3-venv -y
echo "Installing nginx"
sudo apt-get install nginx -y
echo "Creating VM"
python3 -m venv /home/ubuntu/oasis-python/oasis_venv_python
echo "Starting VM"
. oasis_venv_python/bin/activate
pip3 install --no-cache-dir -r requirements.txt
echo "Deactivating VM"
deactivate
echo "Configuring nginx"
sudo ufw allow 'Nginx HTTP'
sudo cp /home/ubuntu/oasis-python/pages/index.html /var/www/demo.oasis-x.io/html/index.html 
sudo cp /home/ubuntu/oasis-python/configs/oasis_python_conf_setup.nginx /etc/nginx/sites-available/demo.oasis-x.io 
sudo ln -s /etc/nginx/sites-available/demo.oasis-x.io /etc/nginx/sites-enabled/ 
sudo cp /home/ubuntu/oasis-python/configs/oasis_python_global.nginx /etc/nginx/nginx.conf 

sudo systemctl restart nginx

echo "TLS Request Encryption (HTTPS only...)"
sudo snap install --classic certbot
sudo certbot --nginx -d demo.oasis-x.io -d www.demo.oasis-x.io
sudo cp /home/ubuntu/oasis-python/configs/oasis_python_secure.nginx /etc/nginx/sites-available/demo.oasis-x.io
sudo systemctl reload nginx
sudo ufw allow 'Nginx Full'
sudo ufw delete allow 'Nginx HTTP'