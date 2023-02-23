#Page for oasis-markets demo
import sys

# import shell modules
import sys
import os

# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
cwd = os.getcwd()
sys.path.append(cwd)
from client_libraries import stripe_markets as transactions

import streamlit as st

import config
client_uri = config.CLIENT_DOMAIN

from PIL import Image


def run():
    st.title("Welcome to the Oasis-Ecosystem API Guide")
    
    image = Image.open('media/welcome_image.png')
    st.image(image)
    st.markdown("Simple tools for managing data collection, process control, and machine learning applications.")
    
    st.subheader("Client Library Quickstart")
    st.write("Get started using the oasis libraries in 3 lines of code:")
    st.code('''git clone https://github.com/oasis-main/oasis-python.git
cd oasis-python
. setup_scripts/env_setup.sh
''', language="bash")

    st.write("This allows API usage from any python interpreter:")
    st.code('''from client_libraries import user_auth, user_txns
user_auth.create_new_user(email, password, admin_id, group_name)''', language='python')
    st.write("To call from a different directory than the library itself, have the calling script execute this line first:")
    st.code('''import sys
sys.path.append("/path/you/git/cloned/into/oasis-python")''', language = 'python')

    st.subheader("Demo Application Quickstart")
    st.write("Spin up a demo version of this app on your local machine:")
    st.code('''git clone https://github.com/oasis-main/oasis-python.git
cd oasis-python
. setup_scripts/env_setup.sh --with_demo
. start.sh
    ''', language="bash")
    st.write("To check that it's working, navigate to http://localhost:8502")



run()