#Page for oasis-auth demo
import sys

# import shell modules
import sys

import streamlit as st
import config
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)


st.set_page_config(page_title=" Oasis-Auth", 
				   page_icon = 'media/icon.png', 
				   layout = "wide")

from client_libraries import user_auth
from utils import results

def run():
#Page title and intro

    st.title("Oasis-Auth (User API)")
    
    contents = st.expander("Table of Contents")
    contents.markdown("[1. Creating New Users](#create-new-user)")
    contents.markdown("[2. User Login w/ Password](#user-password-login)")
    contents.markdown("[3. Getting a User Session](#get-user-session)")
    contents.markdown("[4. Verifying a User Session](#verify-user-session)")
    contents.markdown("[5. Password Reset Requests](#change-user-password)")
    contents.markdown("[6. Delete User (Self)](#delete-user-account)")
    
    admin = st.expander("Admin Settings")
    admin.write("Visit the 👨‍💻 administration page for more info on creating an admin account to manage groups of users.")
    custom_admin = admin.checkbox("Run user authentication with a custom admin and group?", value = False)
    if custom_admin:
        admin_creds = admin.form("Set Admin")
        admin_user_id = admin_creds.text_input("Admin ID")
        group_name = admin_creds.text_input("User Group")
        admin_creds.form_submit_button("Set Admin")
        st.session_state['admin_user_id'] = admin_user_id
        st.session_state['group_name'] = group_name
    else:
        admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2"
        group_name="oasis-users"
        admin.write("Default admin is set to **N3rLUQG4CQNxRNKZ3cBLN8Wli4v2** (ID for hello@oasis-x.io) with the default group as **oasis-users**.")
        admin.write("This info is saved in the background and used in examples as the **admin_id** and **group_name** variables. You can change these variables by checking the box above and entering your own admin user id (not email!) and user group name in the form that pops up.")
        st.session_state['admin_user_id'] = admin_user_id
        st.session_state['group_name'] = group_name






#First endpoint display: /user/create_account
    col_1, col_2 = st.columns(2)
    col_1.subheader("Create New User")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/user/create_account/")
    st.write("*Create a new user in this admin's group. If the user already exists with another admin or group, add them to this admin's group*")
    new_user_form = st.form("Create User")

    email = new_user_form.text_input("Email", help="You'll have to verify this before logging in.")
    password = new_user_form.text_input("Password", type="password")

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Create User")
    if submitted:
        submission = user_auth.create_new_user(email, password, st.session_state["admin_user_id"], st.session_state["group_name"])
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from client_libraries import user_auth #Make sure the environment is set up

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

    email = new_user_form.text_input("Email", help="You'll have to verify this before logging in.", value = st.session_state["user_email"])
    password = new_user_form.text_input("Password", type="password")

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Login")
    if submitted:
        submission = user_auth.password_login(email, password, st.session_state["admin_user_id"], st.session_state["group_name"])
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from client_libraries import user_auth #Make sure the environment is set up

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
    except:
        request_str = user_auth.password_login("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", data={"refresh_token": "placeholder_token"}, url = request_str))


#Third endpoint display: /user/login/session
    col_1, col_2 = st.columns(2)
    col_1.subheader("Get User Session")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/user/login/session/")
    st.write("*Uses the refresh token to obtain a user session, which can be validated to control application access*")
    new_user_form = st.form("Get Session")

    refresh_token = new_user_form.text_input("Refresh Token", help="This will auto-load if you've done the password login above.", value = st.session_state["refresh_token"])

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Get Session")
    if submitted:
        submission = user_auth.get_session(refresh_token, st.session_state["admin_user_id"], st.session_state["group_name"])
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from client_libraries import user_auth #Make sure the environment is set up

session_result = user_auth.get_session(refresh_token, admin_user_id, group_name) # pings authentication server

session_result["attempt"] # "succeeded" or "failed"
session_result["allowed"] # "ok" or "no
session_result["message"] # information about the request
session_result["url"] # url of the web request made to server

session_result["data"]["user_id"] # the user's unique user identifier
session_result["data"]["id_token"] # the user's unique session identifier
""", language = "python") #Leave this off to the left of streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
        #If the above worked it means that we may have some valid values. Let's save them to session state
        st.session_state["user_id"] = submission["data"]["user_id"]
        st.session_state["id_token"] = submission["data"]["id_token"]
    except:
        request_str = user_auth.get_session("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", data={"user_id": "placeholder", "id_token": "placeholder"}, url = request_str))





#Endpoint 4
#This is (or are) the Client Function(s): verify_session(user_id: str, id_token: str, admin_user_id: str, group_name: str)) 
#This is the Resource Location: /user/verify_session
#This is the Demo Interface:  
    col_1, col_2 = st.columns(2)
    col_1.subheader("Verify User Session")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/user/verify_session/")
    st.write("*Uses the the 'id_token' and 'user_id' data from above to validate a user session. Ideal to check access on clients with **limited permission** (iot devices, web browsers, public terminals & displays)*")
    new_user_form = st.form("Verify Session")

    user_id = new_user_form.text_input("User ID", help="This will auto-load if you've done the session login above.", value = st.session_state["user_id"])
    id_token = new_user_form.text_input("Session ID Token", help="This will also auto-load if you've done the session login above ", value = st.session_state["id_token"])

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Verify Session")
    if submitted:
        submission = user_auth.verify_session(user_id, id_token, st.session_state["admin_user_id"], st.session_state["group_name"])
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example 
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from client_libraries import user_auth #Make sure the environment is set up
verification_result = user_auth.verify_session(user_id, id_token, admin_user_id, group_name) # pings authentication server

if verification_result["attempt"] == "succeeded": #make sure you are calling the correct endpoint and inspecting the right object as this is critical to security
    navigate_homepage(user_id) # <- your code goes here
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
        request_str = user_auth.verify_session("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))






#Endpoint 5
#This is (or are) the Client Function(s): user_auth.change_password(email: str, admin_user_id: str, group_name: str)
#This is the Resource Location: /user/change_password/
#This is the Demo Interface: 
    col_1, col_2 = st.columns(2)
    col_1.subheader("Change User Password")
    col_2.write("")
    col_2.write("REST API (POST): https://auth.oasis-x.io/user/change_password/")
    st.write("*Change a user's password from the server. Ideal for when a user has forgotten their login info*")
    new_user_form = st.form("Change Password")

    email = new_user_form.text_input("Email", help="The user's email. We'll send a reset link to their inbox and reset the password")

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Change Password")
    if submitted:
        submission = user_auth.change_password(email, st.session_state["admin_user_id"], st.session_state["group_name"])
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from client_libraries import user_auth #Make sure the environment is set up
change_result = user_auth.change_password(email, admin_user_id, group_name) # pings authentication server

if change_result["attempt"] == "succeeded": #make sure you are calling the correct endpoint and inspecting the right object as this is critical to security
    success() # <- your code goes here
else:
    failure() # <- your code goes here

#You can also do this:

if change_result["allowed"] == "ok": #For security reasons we will never return an attempt == "succeeded" and allowed = "no" in the same message, and vice versa
    print("Password Changed.") #This is to help developers keep things consistent while providing a few areas to 
else:
    print(change_result["message"]) #For more information into the nature of the error, you can inspect the message
    print(change_result["response_code"]) #As well as the http response code: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

#This one doesn't come with any additional data, just the standard response ("attempt","allowed","message","url")
change_result["attempt"] # "succeeded" or "failed"
change_result["allowed"] # "ok" or "no
change_result["message"] # information about the request
change_result["url"] # url of the web request made to server

"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = user_auth.change_password("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))

#Endpoint 6
#This is (or are) the Client Function(s): user_auth.delete_user(user_id: str, password: str, admin_user_id: str, group_name: str)
#This is the Resource Location: /user/delete_account/
#This is the Demo Interface: 
    col_1, col_2 = st.columns(2)
    col_1.subheader("Delete User Account")
    col_2.write("")
    col_2.write("REST API (DELETE): https://auth.oasis-x.io/user/delete_account/")
    st.write("*Delete a user's account from the server. Ideal for when a user no longer needs access to the system*")
    new_user_form = st.form("Delete Account")

    user_id = new_user_form.text_input("User ID", help="The user's ID. We'll use this to identify the user in the system")
    password = new_user_form.text_input("Password", help="The user's password. We'll use this to verify the user's identity")

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Delete Account")
    if submitted:
        submission = user_auth.delete_user(user_id, password, st.session_state["admin_user_id"], st.session_state["group_name"])
        if submission["attempt"] == "succeeded":
            st.success(submission["message"])
        else:
            st.error(submission["message"])

    #Provide a code example
    code_example = st.expander("Code Example (Python)")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code(
"""
from client_libraries import user_auth #Make sure the environment is set up
delete_result = user_auth.delete_user(user_id, password, admin_user_id, group_name) # pings authentication server

if delete_result["attempt"] == "succeeded": #make sure you are calling the correct endpoint and inspecting the right object as this is critical to security
    success() # <- your code goes here
else:
    failure() # <- your code goes here

#You can also do this:

if delete_result["allowed"] == "ok": #For security reasons we will never return an attempt == "succeeded" and allowed = "no" in the same message, and vice versa
    print("Account Deleted.") #This is to help developers keep things consistent while providing a few areas to 
else:
    print(delete_result["message"]) #For more information into the nature of the error, you can inspect the message
    print(delete_result["response_code"]) #As well as the http response code: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status

#This one doesn't come with any additional data, just the standard response ("attempt","allowed","message","url")
delete_result["message"] # information about the request
delete_result["url"] # url of the web request made to server
"""
, language = "python") #Leave this off to the left or streamlit will indent it, unfortunately
    
    #Show how the request is put together
    request_example = st.expander("Request Example (HTTPS)")
    request_example.write("Here's the request URL with parameter values so you use the REST API:")
    try:
        request_str = submission["url"]
    except:
        request_str = user_auth.delete_user("PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER", "PLACEHOLDER")["url"] #This should return a failure, but the URL should be intact
    request_example.write(request_str)
    request_example.write("""Work with a language of your choice by substituting the placeholders or submitted info with your own values. 
Then, using a https library, make an appropriate call to the endpoint. After completing the web request, use a json tool to deserialize the byte response into a native object and access its properties:""")
    try:
        print(submission)
        request_example.write(submission)
    except:
        request_example.write(results.response(True,True,message="This is an example response", url = request_str))
    

run()