import sys
import os


# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
cwd = os.getcwd()
sys.path.append(cwd)

import streamlit as st

def run():
    
    st.sidebar.bottom()
    st.sidebar.collapsible(False)
    st.sidebar.title("Sidebar")
    st.sidebar.text("This is the bottom sidebar")

run()
