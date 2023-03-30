#!/bin/sh -e

#From the application root, I use the following syntax to call
#. setup_scripts/xyz_setup.sh

#Try running this after cd-ing into the setup_scripts folder, and you'll see why I like to use absolute paths
#I am open to finding some other solution that involves a global variable
#We can also pull specific files from github using the git archive command, but I'm not sure how to do that yet
cp ../oasis-auth/clients/user_client.py client_libraries/user_auth.py
cp ../oasis-auth/clients/admin_client.py client_libraries/admin_auth.py 