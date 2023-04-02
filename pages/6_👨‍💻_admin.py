#This uses the admin-auth functionality
import sys
import ast


# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
import config
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)

import streamlit as st
st.set_page_config(page_title=" Oasis-Admin", 
				   page_icon = 'media/icon.png', 
				   layout = "wide")

from clients import admin_auth
from utils import results

#Set session state in case page is refreshed or user otherwise lands on it before initialization
if "admin_user_id" not in st.session_state:
    st.session_state["admin_user_id"] = None
if "group_name" not in st.session_state:
    st.session_state["group_name"] = None
if "admin_refresh_token" not in st.session_state:
    st.session_state["admin_refresh_token"] = None
if "admin_user_id" not in st.session_state:
    st.session_state["admin_user_id"] = None
if "admin_id_token" not in st.session_state:
    st.session_state["admin_id_token"] = None
if "admin_email" not in st.session_state:
    st.session_state["admin_email"] = None

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
    code_example.code("""from clients import admin_auth #Make sure the environment is set up

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
        #Save email for ease of login
        st.session_state["admin_email"] = admin_email
    except:
        request_str = admin_auth.create_admin_account("PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    
    ##Response
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
    code_example.code("""from clients import admin_auth #Make sure the environment is set up

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
#Additional Response Data (submission["data"]): admin_refresh_token
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Admin Login")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/login/password/")
    st.write("*Log in an admin*")
    admin_login_form = st.form("Admin Login")

    admin_email = admin_login_form.text_input("Admin Email", help="The email address of the admin you want to log in.", value = st.session_state["admin_email"])
    admin_password = admin_login_form.text_input("Admin Password", help="The password of the admin you want to log in.", type = "password")

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
    code_example.code("""from clients import admin_auth #Make sure the environment is set up

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
        #Ok, so we have some valid values
        st.session_state["admin_refresh_token"] = submission["data"]["admin_refresh_token"]
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
#Additional Response Data (submission["data"]): admin_user_id, admin_id_token
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Admin Session")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/login/session/")
    st.write("*Get an admin session*")
    admin_session_form = st.form("Admin Session")

    admin_refresh_token = admin_session_form.text_input("Admin Refresh Token", help="The refresh token of the admin you want to get a session for.", value = st.session_state["admin_refresh_token"])

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
    code_example.code("""from clients import admin_auth #Make sure the environment is set up

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
        #Ok, so we have some valid values
        st.session_state["admin_user_id"] = submission["data"]["admin_user_id"]
        st.session_state["admin_id_token"] = submission["data"]["admin_id_token"]
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
#Additional Response Data (submission["data"]): None
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
from clients import admin_auth #Make sure the environment is set up
verification_result = admin_auth.verify_admin_session(admin_user_id, admin_id_token) # pings authentication server

if verification_result["attempt"] == "succeeded": #make sure you are calling the correct endpoint and inspecting the right object as this is critical to security
    navigate_admin_homepage(admin_user_id) # <- your code goes here
else:
    navigate_login(error) # <- your code goes here

#You can also do this:

if verification_result["allowed"] == "ok": #For security reasons we will never return an attempt == "succeeded" and allowed = "no" in the same message, and vice versa
    print("Access Granted.")
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
#Additional Response Data (submission["data"]): None
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Create User Group")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/create_user_group/")
    st.write("*Create a new user group*")
    new_user_group_form = st.form("Create User Group")

    admin_user_id = new_user_group_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = new_user_group_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    new_group_name = new_user_group_form.text_input("New Group Name", help="The name of the new user group you want to create.")
    group_user_params = new_user_group_form.text_input("Group User Parameters", help="A dictionary of default parameters to be associated with the new user group eg. {'payment_plan':'free'}. This is optional.")

    # Every form must have a submit button.
    submitted = new_user_group_form.form_submit_button("Create Group")
    if submitted:
        submission = admin_auth.create_user_group(admin_user_id, admin_id_token, new_group_name, ast.literal_eval(group_user_params))
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
group_creation_result = admin_auth.create_user_group(admin_user_id, admin_id_token, new_group_name, group_user_params) # pings authentication server

#This one doesn't come with any data, just the standard response
group_creation_result["attempt"] # "succeeded" or "failed"
group_creation_result["allowed"] # "ok" or "no

group_creation_result["message"] # information about the request
group_creation_result["url"] # url of the web request made to server
group_creation_result["response_code"] # status of the http request  
"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.create_user_group("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", {})["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/get_user_groups/
#Function: admin_auth.get_admins_groups(admin_user_id: str, admin_id_token: str, return_list = False)
#Additional Response Data (submission["data"]):  groups: list
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Get User Groups")
    col_2.write("")
    col_2.write("REST API (GET): https://auth.oasis-x.io/admin/get_user_groups/")
    st.write("*Get a list of user groups*")
    get_user_groups_form = st.form("Get User Groups")

    admin_user_id = get_user_groups_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = get_user_groups_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])

    # Every form must have a submit button.
    submitted = get_user_groups_form.form_submit_button("Get Groups")
    if submitted:
        submission = admin_auth.get_admins_groups(admin_user_id, admin_id_token)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
group_list_result = admin_auth.get_admins_groups(admin_user_id, admin_id_token) # pings authentication server

#View the admins groups as a list
group_list_result["data"]["groups"] # list of user groups

group_list_result["attempt"] # "succeeded" or "failed"
group_list_result["allowed"] # "ok" or "no
group_list_result["message"] # information about the request
group_list_result["url"] # url of the web request made to server
group_list_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.get_admins_groups("PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/get_group_users/
#Function: admin_auth.get_group_users(admin_user_id: str, admin_id_token: str, group_name: str, return_list = False)
#Additional Response Data (submission["data"]):  users: list
#Demo Interface: 
    col_1, col_2 = st.columns(2)
    col_1.subheader("Get Group Users")
    col_2.write("")
    col_2.write("REST API (GET): https://auth.oasis-x.io/admin/get_group_users/")
    st.write("*Get a list of users in a group*")
    get_group_users_form = st.form("Get Group Users")

    admin_user_id = get_group_users_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = get_group_users_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    group_name = get_group_users_form.text_input("Group Name", help="The name of the group you want to get users from.")

    # Every form must have a submit button.
    submitted = get_group_users_form.form_submit_button("Get Group Users")
    if submitted:
        submission = admin_auth.get_group_users(admin_user_id, admin_id_token, group_name)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
group_users_result = admin_auth.get_group_users(admin_user_id, admin_id_token, group_name) # pings authentication server

#View the users in the group as a list
group_users_result["data"]["users"] # list of users in the group

group_users_result["attempt"] # "succeeded" or "failed"
group_users_result["allowed"] # "ok" or "no
group_users_result["message"] # information about the request
group_users_result["url"] # url of the web request made to server
group_users_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.get_group_users("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/get_uid_by_email/
#Function: admin_auth.get_user_id_by_email(user_email: str, admin_user_id: str, admin_id_token: str, group_name: str)
#Additional Response Data (submission["data"]):  user_id: str
#Demo Interface: 
    col_1, col_2 = st.columns(2)
    col_1.subheader("Get User ID By Email")
    col_2.write("")
    col_2.write("REST API (GET): https://auth.oasis-x.io/admin/get_uid_by_email/")
    st.write("*Get a user's ID by their email address*")
    get_uid_form = st.form("Get User ID By Email")

    admin_user_id = get_uid_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = get_uid_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    user_email = get_uid_form.text_input("User Email", help="The email address of the user you want to get the ID of.")
    group_name = get_uid_form.text_input("Group Name", help="The group the user belongs to.")

    # Every form must have a submit button.
    submitted = get_uid_form.form_submit_button("Get User ID")
    if submitted:
        submission = admin_auth.get_user_id_by_email(user_email, admin_user_id, admin_id_token, group_name)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
user_id_result = admin_auth.get_user_id_by_email(user_email, admin_user_id, admin_id_token, group_name) # pings authentication server

#View the user's ID
user_id_result["data"]["user_id"] # user's ID

user_id_result["attempt"] # "succeeded" or "failed"
user_id_result["allowed"] # "ok" or "no
user_id_result["message"] # information about the request
user_id_result["url"] # url of the web request made to server
user_id_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
        #If the above worked it means that we may have some valid values. Let's save them to session state
        st.session_state["user_id"] = submission["data"]["user_id"]
    except:
        request_str = admin_auth.get_user_id_by_email("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/get_user_email/
#Function: admin_auth.get_user_email(user_id: str, admin_user_id: str, admin_id_token: str, group_name: str)
#Additional Response Data (submission["data"]):  user_email: str
#Demo Interface: 

    col_1, col_2 = st.columns(2)
    col_1.subheader("Get User Email")
    col_2.write("")
    col_2.write("REST API (GET): https://auth.oasis-x.io/admin/get_user_email/")
    st.write("*Get a user's email address by their ID*")
    get_email_form = st.form("Get User Email")

    admin_user_id = get_email_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = get_email_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    user_id = get_email_form.text_input("User ID", help="The ID of the user you want to get the email address of.")
    group_name = get_email_form.text_input("Group Name", help="The group the user belongs to.")

    # Every form must have a submit button.
    submitted = get_email_form.form_submit_button("Get User Email")
    if submitted:
        submission = admin_auth.get_user_email(user_id, admin_user_id, admin_id_token, group_name)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
user_email_result = admin_auth.get_user_email(user_id, admin_user_id, admin_id_token, group_name) # pings authentication server

#View the user's email
user_email_result["data"]["user_email"] # user's email

user_email_result["attempt"] # "succeeded" or "failed"
user_email_result["allowed"] # "ok" or "no
user_email_result["message"] # information about the request
user_email_result["url"] # url of the web request made to server
user_email_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
        #If the above worked it means that we may have some valid values. Let's save them to session state
        st.session_state["user_email"] = submission["data"]["user_email"]
    except:
        request_str = admin_auth.get_user_email("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/read_user/
#Function: admin_auth.read_user_metadata(admin_user_id: str, admin_id_token: str, user_id: str, group: str)
#Additional Response Data (submission["data"]):  user_id: Dict[str,Any]
#Demo Interface: 
    col_1, col_2 = st.columns(2)
    col_1.subheader("Read User Metadata")
    col_2.write("")
    col_2.write("REST API (GET): https://auth.oasis-x.io/admin/read_user/")
    st.write("*Read a user's metadata*")
    read_user_form = st.form("Read User Metadata")

    admin_user_id = read_user_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = read_user_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    user_id = read_user_form.text_input("User ID", help="The ID of the user you want to read metadata from.")
    group = read_user_form.text_input("Group", help="The group the user belongs to.")

    # Every form must have a submit button.
    submitted = read_user_form.form_submit_button("Read User Metadata")
    if submitted:
        submission = admin_auth.read_user_metadata(admin_user_id, admin_id_token, user_id, group)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
user_metadata_result = admin_auth.read_user_metadata(admin_user_id, admin_id_token, user_id, group) # pings authentication server

#View the user's metadata
user_metadata_result["data"]["user_id"] # user's metadata

user_metadata_result["attempt"] # "succeeded" or "failed"
user_metadata_result["allowed"] # "ok" or "no
user_metadata_result["message"] # information about the request
user_metadata_result["url"] # url of the web request made to server
user_metadata_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.read_user_metadata("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/write_user/
#Function: admin_auth.write_user_metadata(admin_user_id: str, admin_id_token: str, user_id: str, group: str, dictionary: Dict[str, Any]): #all dicts passed to fastapi over HTTP must be string representation
#Additional Response Data (submission["data"]):  None
#Demo Interface: 
    col_1, col_2 = st.columns(2)
    col_1.subheader("Write User Metadata")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/write_user/")
    st.write("*Write a user's metadata*")
    write_user_form = st.form("Write User Metadata")

    admin_user_id = write_user_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = write_user_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    user_id = write_user_form.text_input("User ID", help="The ID of the user you want to write metadata to.")
    group = write_user_form.text_input("Group", help="The group the user belongs to.")
    dictionary = write_user_form.text_input("Dictionary", help="The dictionary of metadata you want to write to the user. Must be a string representation of a dictionary.")

    # Every form must have a submit button.
    submitted = write_user_form.form_submit_button("Write User Metadata")
    if submitted:
        submission = admin_auth.write_user_metadata(admin_user_id, admin_id_token, user_id, group, ast.literal_eval(dictionary))
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
user_metadata_result = admin_auth.write_user_metadata(admin_user_id, admin_id_token, user_id, group, dictionary) # pings authentication server

user_metadata_result["attempt"] # "succeeded" or "failed"
user_metadata_result["allowed"] # "ok" or "no
user_metadata_result["message"] # information about the request
user_metadata_result["url"] # url of the web request made to server
user_metadata_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.write_user_metadata("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))


#Endpoint: /admin/user_access_request/
#Function: admin_auth.request_user_access(admin_user_id: str, admin_id_token: str, user_id: str, group: str, data_type: Literal["allowance_count","credit_balance","clearance_code"], field: str, required: str, emissions_kg: float = 0.0000, check_only: bool = False)
#Additional Response Data (submission["data"]): None
#Demo Interface: 
    col_1, col_2 = st.columns(2)
    col_1.subheader("Request User Access")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/user_access_request/")
    st.write("*Request access to a user's data*")
    request_user_form = st.form("Request User Access")

    admin_user_id = request_user_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = request_user_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    user_id = request_user_form.text_input("User ID", help="The ID of the user you want to request access to.")
    group = request_user_form.text_input("Group", help="The group the user belongs to.")
    data_type = request_user_form.selectbox("Data Type", ["allowance_count","credit_balance","clearance_code"])
    field = request_user_form.text_input("Field", help="The field you want to access.")
    required = request_user_form.text_input("Required", help="The required value for the field.")
    emissions_kg = request_user_form.number_input("Emissions (kg)", help="The emissions associated with the request.", value = 0.0000)
    check_only = request_user_form.checkbox("Check Only", help="Check if the request is valid without actually making the request.")

    # Every form must have a submit button.
    submitted = request_user_form.form_submit_button("Request User Access")
    if submitted:
        submission = admin_auth.request_user_access(admin_user_id, admin_id_token, user_id, group, data_type, field, required, emissions_kg, check_only)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
user_access_result = admin_auth.request_user_access(admin_user_id, admin_id_token, user_id, group, data_type, field, required, emissions_kg, check_only) # pings authentication server

user_access_result["attempt"] # "succeeded" or "failed"
user_access_result["allowed"] # "ok" or "no
user_access_result["message"] # information about the request
user_access_result["url"] # url of the web request made to server
user_access_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.request_user_access("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", 0.0000, False)["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/reset_user/
#Function: admin_auth.reset_user(admin_user_id: str, admin_id_token: str, user_id: str, group_name: str)
#Additional Response Data (submission["data"]):  None
#Demo Interface: 
    col_1, col_2 = st.columns(2)
    col_1.subheader("Reset User")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/reset_user/")
    st.write("*Reset a user's data*")
    reset_user_form = st.form("Reset User")

    admin_user_id = reset_user_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = reset_user_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    user_id = reset_user_form.text_input("User ID", help="The ID of the user you want to reset.")
    group_name = reset_user_form.text_input("Group Name", help="The group the user belongs to.")

    # Every form must have a submit button.
    submitted = reset_user_form.form_submit_button("Reset User")
    if submitted:
        submission = admin_auth.reset_user(admin_user_id, admin_id_token, user_id, group_name)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
reset_user_result = admin_auth.reset_user(admin_user_id, admin_id_token, user_id, group_name) # pings authentication server

reset_user_result["attempt"] # "succeeded" or "failed"
reset_user_result["allowed"] # "ok" or "no
reset_user_result["message"] # information about the request
reset_user_result["url"] # url of the web request made to server
reset_user_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.reset_user("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/change_group_schema/
#Function: admin_auth.change_group_schema(admin_user_id: str, admin_id_token: str, group_name: str, new_schema_dict: Dict[str, Any], reset_all: bool)
#Additional Response Data (submission["data"]):  None
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Change Group Schema")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/admin/change_group_schema/")
    st.write("*Change the schema of a group*")
    change_group_schema_form = st.form("Change Group Schema")

    admin_user_id = change_group_schema_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = change_group_schema_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    group_name = change_group_schema_form.text_input("Group Name", help="The group you want to change the schema of.")
    new_schema_dict = change_group_schema_form.text_input("New Schema Dictionary", help="The new schema you want to apply to the group. Must be a valid JSON object.")
    reset_all = change_group_schema_form.checkbox("Reset All", help="Check this box if you want to reset all users in the group to the new schema.")

    # Every form must have a submit button.
    submitted = change_group_schema_form.form_submit_button("Change Group Schema")
    if submitted:
        submission = admin_auth.change_group_schema(admin_user_id, admin_id_token, group_name, new_schema_dict, reset_all)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
change_group_schema_result = admin_auth.change_group_schema(admin_user_id, admin_id_token, group_name, new_schema_dict, reset_all) # pings authentication server

change_group_schema_result["attempt"] # "succeeded" or "failed"
change_group_schema_result["allowed"] # "ok" or "no
change_group_schema_result["message"] # information about the request
change_group_schema_result["url"] # url of the web request made to server
change_group_schema_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.change_group_schema("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", False)["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/delete_user/
#Function: admin_auth.admin_delete_user(admin_user_id: str, admin_id_token: str, user_id: str, group_name: str)
#Additional Response Data (submission["data"]):  None
#Demo Interface:
    col_1, col_2 = st.columns(2)
    col_1.subheader("Delete User")
    col_2.write("")
    col_2.write("REST API (DELETE): https://auth.oasis-x.io/admin/delete_user/")
    st.write("*Delete a user from a group*")
    delete_user_form = st.form("Delete User")

    admin_user_id = delete_user_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = delete_user_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    user_id = delete_user_form.text_input("User ID", help="The user you want to delete.")
    group_name = delete_user_form.text_input("Group Name", help="The group the user is in.")

    # Every form must have a submit button.
    submitted = delete_user_form.form_submit_button("Delete User")
    if submitted:
        submission = admin_auth.admin_delete_user(admin_user_id, admin_id_token, user_id, group_name)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
delete_user_result = admin_auth.admin_delete_user(admin_user_id, admin_id_token, user_id, group_name) # pings authentication server

delete_user_result["attempt"] # "succeeded" or "failed"
delete_user_result["allowed"] # "ok" or "no
delete_user_result["message"] # information about the request
delete_user_result["url"] # url of the web request made to server
delete_user_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.admin_delete_user("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/delete_group/
#Function: admin_auth.delete_group(admin_user_id: str,admin_id_token: str, group_name: str)
#Additional Response Data (submission["data"]):  None
#Demo Interface:

    col_1, col_2 = st.columns(2)
    col_1.subheader("Delete Group")
    col_2.write("")
    col_2.write("REST API (DELETE): https://auth.oasis-x.io/admin/delete_group/")
    st.write("*Delete a group*")
    delete_group_form = st.form("Delete Group")

    admin_user_id = delete_group_form.text_input("Admin User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["admin_user_id"])
    admin_id_token = delete_group_form.text_input("Admin Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["admin_id_token"])
    group_name = delete_group_form.text_input("Group Name", help="The group you want to delete.")

    # Every form must have a submit button.
    submitted = delete_group_form.form_submit_button("Delete Group")
    if submitted:
        submission = admin_auth.delete_group(admin_user_id, admin_id_token, group_name)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
delete_group_result = admin_auth.delete_group(admin_user_id, admin_id_token, group_name) # pings authentication server

delete_group_result["attempt"] # "succeeded" or "failed"
delete_group_result["allowed"] # "ok" or "no
delete_group_result["message"] # information about the request
delete_group_result["url"] # url of the web request made to server
delete_group_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.delete_group("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint: /admin/delete_admin_account/
#Function: admin_auth.delete_admin_account(admin_email: str, admin_password: str)
#Additional Response Data (submission["data"]):  None
#Demo Interface:

    col_1, col_2 = st.columns(2)
    col_1.subheader("Delete Admin Account")
    col_2.write("")
    col_2.write("REST API (DELETE): https://auth.oasis-x.io/admin/delete_admin_account/")
    st.write("*Delete an admin account*")
    delete_admin_account_form = st.form("Delete Admin Account")

    admin_email = delete_admin_account_form.text_input("Admin Email", help="The email of the admin account you want to delete.")
    admin_password = delete_admin_account_form.text_input("Admin Password", help="The password of the admin account you want to delete.")

    # Every form must have a submit button.
    submitted = delete_admin_account_form.form_submit_button("Delete Admin Account")
    if submitted:
        submission = admin_auth.delete_admin_account(admin_email, admin_password)
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from clients import admin_auth #Make sure the environment is set up
delete_admin_account_result = admin_auth.delete_admin_account(admin_email, admin_password) # pings authentication server

delete_admin_account_result["attempt"] # "succeeded" or "failed"
delete_admin_account_result["allowed"] # "ok" or "no
delete_admin_account_result["message"] # information about the request
delete_admin_account_result["url"] # url of the web request made to server
delete_admin_account_result["response_code"] # status of the http request  

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = admin_auth.delete_admin_account("PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

run()