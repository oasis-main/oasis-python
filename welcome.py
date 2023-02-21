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

def run():
    st.title("Welcome to the Oasis-Ecosystem API Guide")
    st.subheader("Browse our demos to the left for easy developer tools w/ quickstart guides.")

run()