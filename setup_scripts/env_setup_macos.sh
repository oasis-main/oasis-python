#!/bin/sh -e

echo "Installing python3"
brew install python3
python -m pip install --upgrade pip

echo "Creating VM"
python3 -m venv ./oasis_venv_python

echo "Starting VM"
. oasis_venv_python/bin/activate
pip3 install -r requirements.txt

if [[ "$1" == "--with_demo" ]]; then pip3 install --no-cache-dir streamlit==1.17.0 && echo "Installed oasis-python client with demo"; else echo "Installed oasis-python client."; fi
