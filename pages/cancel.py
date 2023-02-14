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
  st.title('Subscription creation canceled')

run()