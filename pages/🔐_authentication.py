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
from client_libraries import user_auth

def run():
    st.title("Oasis-Auth Demo (Users)")

    st.subheader("Create New User")
    with st.form("Create User"):
        st.write("Enter an email and password")

        email = st.text_input("Email", help="You'll have to verify this before logging in.")
        password = st.text_input("Password")
        custom_admin = st.checkbox("Test with custom admin credentials?", value = False)
        if custom_admin:
            admin_user_id = st.text_input("Admin ID")
            group_name = st.text_input("User Group")
        else:
            st.write("Default is set to the admin 'hello@oasis-x.io' and group 'oasis-users'")
            admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2"
            group_name="oasis-users"

        # Every form must have a submit button.
        submitted = st.form_submit_button("Create User")
        if submitted:
            submission = user_auth.create_new_user(email, password, admin_user_id, group_name)
            if submission["attempt"] == "succeeded":
                st.success(submission["message"])
            else:
                st.error(submission["message"])

    client_quickstart_1 = st.expander("Client Quickstart")
    with client_quickstart_1:
        st.write("Make sure you have installed the library & demo")
        st.code("")
    
    code_example_1 = st.expander("Demo Server Quickstart")
    with code_example_1:
        st.write("Make sure you have installed the client library o")

    st.subheader("Password Login")

    st.subheader("Get User Session")

    st.subheader("Verify User Session")

    st.subheader("Change User Password")

    st.subheader("User Account Deletion")
    

run()