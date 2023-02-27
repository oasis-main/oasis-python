#This uses the admin-auth functionality
import sys

# import shell modules
import sys

# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
import config
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)

import streamlit as st
st.set_page_config(page_title=" Oasis-Admin", 
				   page_icon = 'media/icon.png', 
				   layout = "wide")

from client_libraries import admin_auth
from utils import results

if "admin_user_id" not in st.session_state:
    st.session_state["admin_user_id"] = None
if "group_name" not in st.session_state:
    st.session_state["group_name"] = None
if "refresh_token" not in st.session_state:
    st.session_state["admin_refresh_token"] = None
if "user_id" not in st.session_state:
    st.session_state["admin_user_id"] = None
if "id_token" not in st.session_state:
    st.session_state["admin_id_token"] = None

def run():
    st.title("Oasis-Auth (Admin API)")

#Function: admin_auth.create_admin_account(admin_email: str, admin_password: str)
#Endpoint: /admin/new_account
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Create New Admin")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/new_account/")
    st.write("*Create a new admin account*")
    new_admin_form = st.form("Create Admin")

    admin_email = new_admin_form.text_input("Admin Email", help="You'll have to verify this before logging in.")
    admin_password = new_admin_form.text_input("Admin Password", type="password")

    # Every form must have a submit button.
    submitted = new_admin_form.form_submit_button("Create Admin")
    if submitted:
        submission = admin_auth.create_admin_account(admin_email, admin_password)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from client_libraries import admin_auth #Make sure the environment is set up

creation_result = admin_auth.create_admin_account(admin_email, admin_password) # pings authentication server

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
    except:
        request_str = admin_auth.create_admin_account("PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/change_password/
#Function: admin_auth.change_admin_password(admin_email: str)
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Change Admin Password")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/change_password/")
    st.write("*Change an admin's password*")
    change_admin_form = st.form("Change Admin Password")

    admin_email = change_admin_form.text_input("Admin Email", help="The email address of the admin whose password you want to change.")

    # Every form must have a submit button.
    submitted = change_admin_form.form_submit_button("Change Password")
    if submitted:
        submission = admin_auth.change_admin_password(admin_email)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from client_libraries import admin_auth #Make sure the environment is set up

change_result = admin_auth.change_admin_password(admin_email # pings authentication server

change_result["attempt"] # "succeeded" or "failed"
change_result["allowed"] # "ok" or "no
change_result["message"] # information about the request
change_result["response_code"] # status code of the https request made to server
change_result["url"] # url of the web request made to server
""", language = "python") #Leave this off to the left of streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you can use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.change_admin_password("PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/login/password/
#Function: admin_auth.admin_login(admin_email: str, admin_password: str, return_tokens = False)
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Admin Login")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/login/password/")
    st.write("*Log in an admin*")
    admin_login_form = st.form("Admin Login")

    admin_email = admin_login_form.text_input("Admin Email", help="The email address of the admin you want to log in.")
    admin_password = admin_login_form.text_input("Admin Password", help="The password of the admin you want to log in.")

    # Every form must have a submit button.
    submitted = admin_login_form.form_submit_button("Log In")
    if submitted:
        submission = admin_auth.admin_login(admin_email, admin_password)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from client_libraries import admin_auth #Make sure the environment is set up

login_result = admin_auth.admin_login(admin_email, admin_password) # pings authentication server

login_result["attempt"] # "succeeded" or "failed"
login_result["allowed"] # "ok" or "no
login_result["message"] # information about the request
login_result["response_code"] # status code of the https request made to server
login_result["url"] # url of the web request made to server

login_result["data"]["admin_refresh_token"] # api token for obtaining user sessions 
""", language = "python") #Leave this off to the left of streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you can use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.admin_login("PLACEHOLDER","PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/login/session/
#Function: admin_auth.get_admin_session(admin_refresh_token: str, return_tokens = False):
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Admin Session")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/login/session/")
    st.write("*Get an admin session*")
    admin_session_form = st.form("Admin Session")

    admin_refresh_token = admin_session_form.text_input("Admin Refresh Token", help="The refresh token of the admin you want to get a session for.")

    # Every form must have a submit button.
    submitted = admin_session_form.form_submit_button("Get Session")
    if submitted:
        submission = admin_auth.get_admin_session(admin_refresh_token)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from client_libraries import admin_auth #Make sure the environment is set up

session_result = admin_auth.get_admin_session(admin_refresh_token) # pings authentication server

session_result["attempt"] # "succeeded" or "failed"
session_result["allowed"] # "ok" or "no
session_result["message"] # information about the request
session_result["response_code"] # status code of the https request made to server
session_result["url"] # url of the web request made to server

session_result["data"]["admin_user_id"] # the user's unique user identifier
session_result["data"]["admin_id_token"] # the user's unique session identifier
""", language = "python") #Leave this off to the left of streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you can use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.get_admin_session("PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/verify_session/
#Function: admin_auth.verify_admin_session(admin_user_id: str, admin_id_token: str)
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Verify Admin Session")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/verify_session/")
    st.write("*Uses the the 'admin_id_token' and 'admin_user_id' data from above to validate an admin session. Ideal to check access on clients with **full permission** (admin consoles, server-side applications, etc)*")
    new_user_form = st.form("Verify Session")

    admin_user_id = new_user_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = new_user_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Verify Session")
    if submitted:
        submission = admin_auth.verify_admin_session(admin_user_id, admin_id_token)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from client_libraries import admin_auth #Make sure the environment is set up
verification_result = admin_auth.verify_admin_session(admin_user_id, admin_id_token) # pings authentication server

if verification_result["attempt"] == "succeeded": #make sure you are calling the correct endpoint and inspecting the right object as this is critical to security
    navigate_admin_homepage(admin_user_id) # <- your code goes here
else:
    navigate_login(error) # <- your code goes here

#You can also do this:

if verification_result["allowed"] == "ok": #For security reasons we will never return an attempt == "succeeded" and allowed = "no" in the same message, and vice versa
    print("Access Granted.") #This is to help developers 
else:
    print(verification_result["message"]) #For more information into the nature of the error, you can inspect the message
    print(verification_result["response_code"]) #As well as the http response code: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

#This one doesn't come with any data, just the standard response
verification_result["attempt"] # "succeeded" or "failed"
verification_result["allowed"] # "ok" or "no
verification_result["message"] # information about the request
verification_result["url"] # url of the web request made to server
"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.verify_admin_session("PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/create_user_group/
#Function: admin_auth.create_user_group(admin_user_id: str, admin_id_token: str, new_group_name: str, group_user_params: Dict[str, Any] = {})
#Demo Interface:

#Endpoint: /admin/get_user_groups/
#Function: admin_auth.get_admins_groups(admin_user_id: str, admin_id_token: str, return_list = False)
#Demo Interface:

#Endpoint: /admin/get_group_users/
#Function: admin_auth.get_group_users(admin_user_id: str, admin_id_token: str, group_name: str, return_list = False)
#Demo Interface:

#Endpoint: /admin/read_user/
#Function: admin_auth.read_user_metadata(admin_user_id: str, admin_id_token: str, user_id: str, group: str)
#Demo Interface:

#Endpoint: /admin/write_user/
#Function: admin_auth.write_user_metadata(admin_user_id: str, admin_id_token: str, user_id: str, group: str, dictionary: Dict[str, Any]): #all dicts passed to fastapi over HTTP must be string representation
#Demo Interface:

#Endpoint: /admin/user_access_request/
#Function: admin_auth.request_user_access(admin_user_id: str, admin_id_token: str, user_id: str, group: str, data_type: Literal["allowance_count","credit_balance","clearance_code"], field: str, required: str, emissions_kg: float = 0.0000, check_only: bool = False)
#Demo Interface:

#Endpoint: /admin/reset_user/
#Function: admin_auth.reset_user(admin_user_id: str, admin_id_token: str, user_id: str, group_name: str)
#Demo Interface:

#Endpoint: /admin/change_group_schema/
#Function: admin_auth.change_group_schema(admin_user_id: str, admin_id_token: str, group_name: str, new_schema_dict: Dict[str, Any], reset_all: bool)
#Demo Interface:

#Endpoint: /admin/delete_user/
#Function: admin_auth.admin_delete_user(admin_user_id: str, admin_id_token: str, user_id: str, group_name: str)
#Demo Interface:

#Endpoint: /admin/delete_group/
#Function: admin_auth.delete_group(admin_user_id: str,admin_id_token: str, group_name: str)
#Demo Interface:

#Endpoint: /admin/delete_admin_account/
#Function: admin_auth.delete_admin_account(admin_email: str, admin_password: str)
#Demo Interface:

run()