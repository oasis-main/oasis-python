import sys
import json
import httpx

import requests

# import shell modules
import sys
import os

# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
cwd = os.getcwd()
sys.path.append(cwd)
import lib

import streamlit as st
import streamlit.components.v1 as components

def run():
    st.title('Add New Customer')

    name = st.text_input('Name')
    oasis_x_id = st.text_input('Oasis-X Id')
    email_addr = st.text_input('Email Address')
    
    if st.button('Create Customer'):
        #Stripe unit amounts are specified in cents, and are best passed as integers
        new_customer = lib.create_customer(oasis_x_id, email_addr, name)
        print(f'{new_customer}')

run()