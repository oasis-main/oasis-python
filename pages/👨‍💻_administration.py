#This uses the admin-auth functionality
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

def run():
    st.title("Oasis-Authe Demo (Admins)")
    
    st.subheader("Create Admin Account")
    st.tite("")

    st.subheader("Change Admin Password")
    st.tite("")

    st.subheader("Admin Login")
    st.tite("")

    st.subheader("Get Admin Session")
    st.tite("")

    st.subheader("Verify Admin Session")
    st.tite("")

    st.subheader("Create User Group")
    st.tite("")

    st.subheader("Get Admins Groups")
    st.tite("")

    st.subheader("Get Group Users")
    st.tite("")

    st.subheader("Read User Metadata")
    st.tite("")

    st.subheader("Write User Metadata")
    st.tite("")

    st.subheader("Request User Access")
    st.tite("")

    st.subheader("Reset User")
    st.tite("")

    st.subheader("Change Group Schema")
    st.tite("")

    st.subheader("Admin Delete User")
    st.tite("")

    st.subheader("Delete Group")
    st.tite("")

    st.subheader("Delete Admin Account")
    st.tite("")
