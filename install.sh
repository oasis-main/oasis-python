echo "Installing uvicorn"
sudo apt-get install uvicorn -y #FastAPI Runtime
echo "Installing python3-pip"
sudo apt-get install python3-pip -y
echo "Installing python3-venv"
sudo apt-get install python3-venv -y
echo "Installing nginx"
sudo apt-get install nginx -y
echo "Creating VM"
python3 -m venv /home/ubuntu/oasis-markets/oasis_venv_markets
echo "Starting VM"
. oasis_venv_markets/bin/activate
pip3 install --no-cache-dir -r requirements.txt
streamlit run streamlit_stripe_demo.py