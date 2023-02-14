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
    intervals={
        'Yearly': 'year',
        'Monthly':'month',
        'Weekly':'week',
        'Daily': 'day'
    }

    st.title('Add New Oasis-X Subscription Product')

    name = st.text_input('Name')
    description = st.text_input('Description')
    price = st.number_input('Price')
    interval = st.selectbox('Billing Interval',intervals.keys())

    if st.button('Create Product'):
        #Stripe unit amounts are specified in cents, and are best passed as integers
        unit_amount = int(price * 100)
        new_product = lib.create_product(unit_amount, name, description, intervals.get(interval))

run()