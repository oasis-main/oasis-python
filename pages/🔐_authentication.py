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
    st.title("Oasis-Authe Demo (Users)")

    st.subheader("Create New User")

    st.subheader("Change Password")

    st.subheader("Password Login")

    st.subheader("Get Session")

    st.subheader("Verify Session")

    st.subheader("Delete User")
    

run()