#Page for oasis-markets demo
import sys
import os


import streamlit as st
st.set_page_config(page_title=" Oasis-Markets", 
                   page_icon = 'media/icon.png', 
                   layout = "wide")


import config
client_uri = config.CLIENT_DOMAIN
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)

from clients import admin_txns as transactions
from clients import admin_auth as admin_auth
from clients import user_auth as user_auth
from utils import results

#Set session state in case page is refreshed or user otherwise lands on it before initialization
if "admin_user_id" not in st.session_state:
    st.session_state["admin_user_id"] = ""
if "group_name" not in st.session_state:
    st.session_state["group_name"] = ""
if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = ""
if "user_id" not in st.session_state:
    st.session_state["user_id"] = ""
if "id_token" not in st.session_state:
    st.session_state["id_token"] = ""
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "metadata" not in st.session_state:
    st.session_state["metadata"] = {
        "stripe_customer_id": ""
    }
if "customer" not in st.session_state:
    st.session_state["customer"] = {}
if "customer_subscriptions" not in st.session_state:
    st.session_state["customer_subscriptions"] = []

def run():
    st.title('Oasis-X Markets Admin Portal')

    #Admin
    admin = st.expander("Admin Settings")
    admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2"
    group_name="oasis-users"
    admin.write("Admin user information should not be required for transactions demos, as transactions should function autonomously.")
    if "admin_user_id" not in st.session_state or st.session_state['admin_user_id'] == None:
        st.session_state['admin_user_id'] = admin_user_id
    if "group_name" not in st.session_state or st.session_state['group_name'] == None:
        st.session_state['group_name'] = group_name

    #First endpoint display: /user/create_account
    col_1, col_2 = st.columns(2)
    col_1.subheader("Create New User")
    col_2.write("")
    col_2.write("REST API (POST): https://markets.oasis-x.io/user/create_account/")
    st.write("*Create a new user in your Oasis-Market Admin group. If the user already exists with another admin or group, add them to this admin's group*")
    new_user_form = st.form("Create User")

    email = new_user_form.text_input("Email", help="You'll have to verify this before logging in.")
    password = new_user_form.text_input("Password", type="password")

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Create User")
    if submitted:
        submission = transactions.create_new_user(email, password)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from clients import user_auth #Make sure the environment is set up

creation_result = user_auth.create_new_user(email, password, admin_user_id, group_name) # pings authentication server

creation_result["attempt"] # "succeeded" or "failed"
creation_result["allowed"] # "ok" or "no
creation_result["message"] # information about the request
creation_result["response_code"] # status code of the https request made to server
creation_result["url"] # url of the web request made to server
""", language = "python") #Leave this off to the left of streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you can use the REST API:")
    try:
        request_str = submission["url"]
        #If the above worked it means that we may have some valid values. Let's save them to session state
        #Save email for ease of login
        st.session_state["user_email"] = email
    except:
        request_str = user_auth.create_new_user("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Second endpoint display: /user/login/password
    col_1, col_2 = st.columns(2)
    col_1.subheader("User Password Login")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/user/login/password/")
    st.write("*Submit a valid username and password to get a refresh token, which is can be used to obtain a temporary user session*")
    new_user_form = st.form("Login")
    email = new_user_form.text_input("Email", help="You'll have to verify this before logging in.")
    password = new_user_form.text_input("Password", type="password")
    submitted = new_user_form.form_submit_button("Login")
    if submitted:
        submission = transactions.password_login(email, password)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
            refresh_token = submission["data"]["refresh_token"]
            st.session_state["refresh_token"] = refresh_token
            create_session_r = transactions.create_user_session(refresh_token)
            if create_session_r["attempt"] == "succeeded":
                st.success(create_session_r["message"])
                user_id = create_session_r["data"]["user_id"]
                id_token = create_session_r["data"]["id_token"]
                st.session_state["user_id"] = user_id
                st.session_state["id_token"] = id_token
                metadata_r = transactions.read_user_metadata(user_id)
                if metadata_r["attempt"] == "succeeded":
                    st.success(metadata_r["message"])
                    data = metadata_r["data"][user_id]
                    print(f"data: {data}")
                    if "stripe_customer_id" in data and data["stripe_customer_id"]:
                        stripe_customer_id = data["stripe_customer_id"]
                        print(f"retriving stripe_customer_id: {stripe_customer_id}")
                        customer_r = transactions.get_customer_by_stripe_id(stripe_customer_id)
                        #Get customer data
                        if customer_r["attempt"] == "succeeded":
                            print(f"customer_r: {customer_r}")
                            customer = customer_r["data"]
                            st.session_state["customer"] = customer
                        else:
                            st.error(customer_r["message"])
                        #Get subscription data
                        # customer_subscription_r = transactions.list_customer_subscriptions(stripe_customer_id)
                        # if customer_subscription_r["attempt"] == "succeeded":
                        #     customer_subscriptions = customer_subscriptions_r["data"]
                        #     st.session_state["customer_subscriptions"] = customer_subscriptions
                        # else:
                        #     st.error(customer_subscription_r["message"])
                else:
                    st.error(metadata_r["message"])
            else: st.error(create_session_r["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from clients import user_auth #Make sure the environment is set up

login_result = user_auth.password_login(email, password, admin_user_id, group_name) # pings authentication server

login_result["attempt"] # "succeeded" or "failed"
login_result["allowed"] # "ok" or "no
login_result["message"] # information about the request
login_result["data"]["refresh_token"] # api token for obtaining user sessions 
""", language = "python") #Leave this off to the left of streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
        #If the above worked it means that we may have some valid values. Let's save them to session state
        st.session_state["user_email"] = email
        st.session_state["refresh_token"] = submission["data"]["refresh_token"]
        user_id = admin_auth.get_user_id_by_email(st.session_state["user_email"], st.session_state["admin_user_id"], st.session_state["admin_id_token"], st.session_state["group_name"])
        st.session_state["user_id"] = user_id
    except:
        request_str = user_auth.password_login("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", data={"refresh_token": "placeholder_token"}, url = request_str))

    #Third endpoint display: /customer/create
    col_1, col_2 = st.columns(2)
    col_1.subheader("Create Stripe Customer")
    col_2.write("")
    col_2.write("REST API (POST): https://markets.oasis-x.io/account/create/")
    st.write("*Create a Stripe Customer object for the logged in user. Customers represent users who will be charged by Oasis-X.*")
    new_customer_form = st.form("Create Stripe Customer")
    if st.session_state["customer"]: 
        new_customer_form.write("A stripe customer has already been created for this user")
        name = new_customer_form.text_input("Name", disabled=True, value=st.session_state.customer["name"])
        email = new_customer_form.text_input("Email", disabled=True, value=st.session_state.customer["email"])
        user_id = new_customer_form.text_input("Oasis-X User ID", disabled=True, value=st.session_state.customer.metadata["oasis_x_id"])
    else:
        name = new_customer_form.text_input("Name")
        email = new_customer_form.text_input("Email", disabled=True, value=st.session_state["user_email"])
        user_id = new_customer_form.text_input("Oasis-X User ID", disabled=True, value=st.session_state["user_id"])
        submitted = new_customer_form.form_submit_button("Create Customer")
        if submitted:
            submission = transactions.create_customer(user_id, email, name)
            #Need to add attempt/allowed/message pattern to transactions api responses
            print(f"customer creation submission:{submission}")
            if submission and submission["id"]:
                stripe_customer_id = submission["id"]
                st.session_state.metadata["stripe_customer_id"] = stripe_customer_id
                save_customer_id_r = transactions.write_user_metadata(user_id, st.session_state.metadata)
                print(f"save_customer_id_r: {save_customer_id_r}")
                if save_customer_id_r["attempt"] == "succeeded":   
                    st.success(save_customer_id_r)
                else:
                    str.error(save_customer_id_r)
            else:
                st.error(submission)

    #Fourth endpoint display: /subscription/create/ and /subscription/update/
    col_1, col_2 = st.columns(2)
    col_1.subheader("Create Subscription")
    col_2.write("")
    col_2.write("REST API (POST): https://markets.oasis-x.io/account/create/")
    st.write("*Create a Stripe Subscription object for the logged in user.*")
    new_subscription_form = st.form("Create Subscription")
    if st.session_state["customer_subscriptions"]: 
        new_subscription_form.write("Existing subscriptions:")
        name = new_subscription_form.text_input("Name", disabled=True, value=st.session_state.customer["name"])
        email = new_subscription_form.text_input("Email", disabled=True, value=st.session_state.customer["email"])
        user_id = new_subscription_form.text_input("Oasis-X User ID", disabled=True, value=st.session_state.customer.metadata["oasis_x_id"])
    # else:
    #     name = new_customer_form.text_input("Name")
    #     email = new_customer_form.text_input("Email", disabled=True, value=st.session_state["user_email"])
    #     user_id = new_customer_form.text_input("Oasis-X User ID", disabled=True, value=st.session_state["user_id"])
    #     submitted = new_customer_form.form_submit_button("Create Customer")
    #     if submitted:
    #         submission = transactions.create_customer(user_id, email, name)
    #         #Need to add attempt/allowed/message pattern to transactions api responses
    #         print(f"subscription creation submission:{submission}")
    #         if submission and submission["id"]:
    #             stripe_subscription_id = submission["id"]
    #             st.session_state.metadata["stripe_subscription_id"] = stripe_subscription_id
    #             save_subscription_id_r = transactions.write_user_metadata(user_id, st.session_state.metadata)
    #             print(f"save_customer_id_r: {save_customer_id_r}")
    #             if save_customer_id_r["attempt"] == "succeeded":   
    #                 st.success(save_customer_id_r)
    #             else:
    #                 str.error(save_customer_id_r)
    #         else:
    #             st.error(submission)
    
    #Fifth endpoint display: /account/create
    col_1, col_2 = st.columns(2)
    col_1.subheader("Create Stripe Account and Account Link")
    col_2.write("")
    col_2.write("REST API (POST): https://markets.oasis-x.io/account/create/")
    st.write("*Create a Stripe account object and associated Stripe account link object.*")
    st.write("*These objects are created even if a user already has Stripe login credentials, with the account representing a parent object for storing information about activity on Oasis-X, and the account link being a temporary object which serves to facilitate linkage between Oasis-X and Stripe.*")
    st.write("*Accounts are only required for users which will receive payments, e.g. in a user-to-user marketplace transaction.*")
    new_account_form = st.form("Create Stripe Account and Link")
    # if "user_id" not in st.session_state or st.session_state.user_id == None or \
    #     "user_email" not in st.session_state or st.session_state.user_email == None:
    #     email = new_user_form.text_input("Email", disabled=True, value="Please login on the authentication page to proceed")
    # else:
    email = new_account_form.text_input("Email", disabled=True, value=st.session_state["user_email"])
    user_id = new_account_form.text_input("Oasis-X User ID", disabled=True, value=st.session_state["user_id"])
    # Every form must have a submit button.
    submitted = new_account_form.form_submit_button("Create Account Link")
    if submitted:
        submission = transactions.create_stripe_account(email,user_id)
        #Need to add attempt/allowed/message pattern to transactions api responses
        print(f"account creation submission:{submission}")
        if submission and submission["redirect_url"]:
            stripe_link = submission["redirect_url"]
            st.success(stripe_link)
        else:
            st.error(submission)


    prices = transactions.list_prices()
    customers = transactions.list_customers()
    st.write('Prices:')
    st.dataframe(prices)

    st.write('Customers:')
    st.dataframe(customers)


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