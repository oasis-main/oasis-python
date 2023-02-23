#Page for oasis-auth demo
import sys

# import shell modules
import sys
import os

# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
cwd = os.getcwd()
sys.path.append(cwd)

import streamlit as st

st.set_page_config(page_title=" Oasis-X", 
				   page_icon = 'media/icon.png', 
				   layout = "wide")

from client_libraries import user_auth
from utils import markdown_fns
from utils import results

def run():
    st.title("Oasis-Auth Demo (Users)")
    custom_admin = st.checkbox("Test user authentication with a custom admin and group?", value = False)
    st.write("Default is set to the admin 'hello@oasis-x.io' and group 'oasis-users'.")
    st.write("Visit the 👨‍💻 administration page for more info on creating an admin account to manage groups of users.")

    st.subheader("Create New User")
    left_col, right_col = st.columns(2)
    new_user_form = left_col.form("Create User")
    new_user_form.write("Enter an email and password")

    email = new_user_form.text_input("Email", help="You'll have to verify this before logging in.")
    password = new_user_form.text_input("Password")
    
    if custom_admin:
        admin_user_id = new_user_form.text_input("Admin ID")
        group_name = new_user_form.text_input("User Group")
    else:
        admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2"
        group_name="oasis-users"

    # Every form must have a submit button.
    submitted = new_user_form.form_submit_button("Create User")
    if submitted:
        submission = user_auth.create_new_user(email, password, admin_user_id, group_name)
        if submission["attempt"] == "succeeded":
            left_col.success(submission["message"])
        else:
            left_col.error(submission["message"])

    code_example = right_col.expander("Code Example")
    code_example.write("Here's how to imlement this in your app using the oasis-python library:")
    code_example.code("""from client_libraries import user_auth #Make sure the environment is set up
login_result = user_auth.create_new_user(email, password, admin_user_id, group_name) # pings authentication server
login_result["attempt"] # "succeeded" or "failed"
login_result["allowed"] # "ok" or "no
login_result["message"] # information about the request
login_result["data"]["refresh_token"] # api token for obtaining user sessions 
""", language = "python") #Leave this off to the left of streamlit will indent it, unfortunately
    
    request_example = right_col.expander("Request Example")
    request_example.write("Not a python user? No problem. Here's the request URL with parameters in bold so you use the bare REST API instead:")
    try:
        request_str = submission["url"]
        #color_map = {email: "red", password: "orange", admin_user_id: "blue", group_name: "green"}
    except:
        request_str = user_auth.create_new_user("[email]", "[password]", "[admin_user_id]", "[group_name]")["url"] #This should return a failure, but the URL should be intact
        #color_map = {"email": "red", "password": "orange", "admin_user_id": "blue", "group_name": "green"}
    
    #for variable in color_map:
    #    request_str = request_str.replace(variable, markdown_fns.bold_color(variable, color_map[variable]))
    request_example.code(request_str)
    request_example.write("Work with your language of choice (javascript, c++, java, c#, rust, bash, etc.) by substituting the bracket segments of the address with your own variables, then making the https request with a built-in library.")
    
    request_example.write("After making the request, use a tool of your choice to deserialize the byte response into a valid json object and access its properties. Here is the raw response:")
    try:
        request_example.code(submission, language = "json")
    except:
        request_example.code(str(results.response(True,True,message="This is an example response", data={"refresh_token": "QwErTyUiOpAsdDfGhJkLzXcVbNm"}, url = request_str)), language = "json")

    st.subheader("Password Login")

    st.subheader("Get User Session")

    st.subheader("Verify User Session")

    st.subheader("Change User Password")

    st.subheader("User Account Deletion")
    

run()