#Page for oasis-markets demo
import sys
import os


import config
client_uri = config.CLIENT_DOMAIN
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)
import streamlit as st
st.set_page_config(page_title=" Oasis-Markets", 
                   page_icon = 'media/icon.png', 
                   layout = "wide")

from client_libraries import admin_txns as transactions




def run():
    st.title('Oasis-X Markets Admin Portal')

    st.write(st.session_state[''])
    
    #First endpoint display: /account/create
    col_1, col_2 = st.columns(2)
    col_1.subheader("Create Account and Account Link")
    col_2.write("")
    col_2.write("REST API (POST): https://markets.oasis-x.io/account/create/")
    st.write("*Create a Stripe account object and associated Stripe account link object. These objects are created even if a user already has Stripe login credentials, with the account representing a parent object for storing information about activity on Oasis-X, and the account link being a temporary object which serves to facilitate linkage between Oasis-X and Stripe.*")
    new_user_form = st.form("Create Stripe Account and Link")

    if "user_id" not in st.session_state or \
        "id_token" not in st.session_state or \
        "user_email" not in st.session_state:
        email = new_user_form.text_input("Email", disabled=True, value="Please login on the authentication page to proceed")
    else:
        email = new_user_form.text_input("Email", disabled=True, value=st.session_state["user_email"])

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Create Account Link")
    if submitted:
        submission = admin_txns.create_account(email, password, st.session_state["admin_user_id"], st.session_state["group_name"])
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])




    prices = transactions.list_prices()
    customers = transactions.list_customers()
    st.write('Prices:')
    st.dataframe(prices)

    st.write('Customers:')
    st.dataframe(customers)


    st.subheader('Add New Customer')

    name = st.text_input('Name')
    oasis_x_id = st.text_input('Oasis-X Id')
    email_addr = st.text_input('Email Address')
    
    if st.button('Create Customer'):
        #Stripe unit amounts are specified in cents, and are best passed as integers
        new_customer = transactions.create_customer(oasis_x_id, email_addr, name)
        print(f'{new_customer}')


    st.subheader('Add New Oasis-X Subscription Product')
    
    intervals={
        'Yearly': 'year',
        'Monthly':'month',
        'Weekly':'week',
        'Daily': 'day'
    }

    description = st.text_input('Description')
    price = st.number_input('Price')
    interval = st.selectbox('Billing Interval',intervals.keys())

    if st.button('Create Product'):
        #Stripe unit amounts are specified in cents, and are best passed as integers
        unit_amount = int(price * 100)
        new_product = transactions.create_product(unit_amount, name, description, intervals.get(interval))

    st.subheader('Add New Subscription')
    stripe_prices = transactions.list_prices()
    formatted_prices = {}
    for sp in stripe_prices:
        key = sp.get('product').get('name') + ' - $' + str(sp.get('unit_amount') / 100) + '0/' + sp.get('recurring').get('interval')
        formatted_prices[key] = sp
    price_list = formatted_prices.keys()

    stripe_customers = transactions.list_customers()
    formatted_customers = {}
    for sc in stripe_customers:
        key = sc.get('metadata').get('oasis_x_id') + ' - ' + sc.get('email')
        formatted_customers[key] = sc
    customer_list = formatted_customers.keys()


    price_key = st.selectbox('Price',price_list)
    customer_key = st.selectbox('Customer',customer_list)
    
    if st.button('Checkout'):
        #Stripe unit amounts are specified in cents, and are best passed as integers
        # new_customer = transactions.create_subscription(oasis_x_id, email_addr, name)
        customer = formatted_customers.get(customer_key)
        customer_id = customer['id']
        price = formatted_prices.get(price_key)
        price_id = price['id']
        items = transactions.create_line_item(price_id)
        mode = 'subscription'
        success_url = client_uri + '/success'
        cancel_url = client_uri + '/cancel'
        checkout_session = transactions.create_checkout_session(price_id, 1, mode, success_url, cancel_url)
        print(f'checkout_session: {checkout_session}')
        
        link='Complete checkout [here](' + checkout_session.get('url') + ')'
        st.markdown(link,unsafe_allow_html=True)

    st.subheader("Subscription Settings")
    
    st.subheader("Subscribe Success")
    st.code("No content")

    st.subheader("Cancel Subscription")
    st.code("No content")

run()