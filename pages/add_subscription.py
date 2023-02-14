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
import config
import streamlit as st
import streamlit.components.v1 as components

client_uri = config.CLIENT_DOMAIN

def run():
    st.title('Add New Subscription')
    stripe_prices = lib.list_prices()
    formatted_prices = {}
    for sp in stripe_prices:
        key = sp.get('product').get('name') + ' - $' + str(sp.get('unit_amount') / 100) + '0/' + sp.get('recurring').get('interval')
        formatted_prices[key] = sp
    price_list = formatted_prices.keys()

    stripe_customers = lib.list_customers()
    formatted_customers = {}
    for sc in stripe_customers:
        key = sc.get('metadata').get('oasis_x_id') + ' - ' + sc.get('email')
        formatted_customers[key] = sc
    customer_list = formatted_customers.keys()


    price_key = st.selectbox('Price',price_list)
    customer_key = st.selectbox('Customer',customer_list)
    
    if st.button('Checkout'):
        #Stripe unit amounts are specified in cents, and are best passed as integers
        # new_customer = lib.create_subscription(oasis_x_id, email_addr, name)
        customer = formatted_customers.get(customer_key)
        customer_id = customer['id']
        price = formatted_prices.get(price_key)
        price_id = price['id']
        items = lib.create_line_item(price_id)
        mode = 'subscription'
        success_url = client_uri + '/success'
        cancel_url = client_uri + '/cancel'
        checkout_session = lib.create_checkout_session(price_id, 1, mode, success_url, cancel_url)
        print(f'checkout_session: {checkout_session}')
        
        link='Complete checkout [here](' + checkout_session.get('url') + ')'
        st.markdown(link,unsafe_allow_html=True)

run()