#Page for oasis-markets demo
import sys

# import shell modules
import sys
import os

# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
cwd = os.getcwd()
sys.path.append(cwd)
from client_libraries import admin_txns as transactions

import streamlit as st
st.set_page_config(page_title=" Oasis-X", 
				   page_icon = 'media/icon.png', 
				   layout = "wide")

import config
client_uri = config.CLIENT_DOMAIN

from PIL import Image

def run():
    st.title("Oasis-Ecosystem API Demo")
    
    st.markdown("Simple developer tools for managing data collection, process control, and machine learning applications.")
    image = Image.open('media/welcome_image.png')
    st.image(image)
    
    st.subheader("Client Quickstart")
    col1, col2 = st.columns([3,1])
    
    operating_system = col2.radio("What operating system are you using?", ["Linux", "MacOS"], index = 0)
    
    col1.write("Get started using the library with 3 lines of code:")
    
    if operating_system == "Linux":
        col1.code('''git clone https://github.com/oasis-main/oasis-python.git
cd oasis-python
. setup_scripts/env_setup_linux.sh
''', language="bash") #Python streamlit code has to be "against the wall" as it indents weirdly otherwise
    
    if operating_system == "MacOS":
        col1.code('''git clone https://github.com/oasis-main/oasis-python.git
cd oasis-python
. setup_scripts/env_setup_macos.sh
''', language="bash")

    col1.write("This allows API usage from any python interpreter, like so:")
    
    col1.code('''from client_libraries import user_auth, user_txns
user_auth.create_new_user(email, password, admin_id, group_name)''', language='python')
    
    col1.write("To call from a different directory than the library itself, have the importing script execute this line first:")
    
    col1.code('''import sys
sys.path.append("/path/you/git/cloned/into/oasis-python")
from client_libraries import user_auth''', language = 'python')

    col1.write("You may also make REST API calls to the various services, documented at: ")
    col1.code('''https://auth.oasis-x.io/docs
https://markets.oasis-x.io/docs''')

    st.subheader("Demo Quickstart")
    st.write("This app is open-source. To spin up a demo version on your local machine:")
    
    if operating_system == "Linux":
        st.code('''git clone https://github.com/oasis-main/oasis-python.git
cd oasis-python
. setup_scripts/env_setup_linux.sh --with_demo
. start.sh
    ''', language="bash")
    if operating_system == "MacOS":
        st.code('''git clone https://github.com/oasis-main/oasis-python.git
cd oasis-python
. setup_scripts/env_setup_macos.sh --with_demo
. start.sh
    ''', language="bash")

    st.write("To check that it's working, navigate to http://localhost:8502")


run()