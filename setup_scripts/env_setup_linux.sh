#!/bin/sh -e
echo "Installing python3-pip"
sudo apt-get install python3-pip -y

echo "Installing python3-venv"
sudo apt-get install python3-venv -y

echo "Creating VM"
python3 -m venv ./oasis_venv_python

echo "Starting VM"
. oasis_venv_python/bin/activate
pip3 install --no-cache-dir -r requirements.txt

if [[ "$1" == "--with_demo" ]]; then pip3 install --no-cache-dir streamlit==1.17.0 && echo "Installed oasis-python client with demo"; else echo "Installed oasis-python client."; fi