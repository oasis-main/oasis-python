#Administrator account clients
#for managing groups of users
import time
import sys
import os
import orjson
import httpx
from datetime import datetime

cwd = os.getcwd()
sys.path.append(cwd)
import config
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)

from typing import Dict, Any

from client_libraries import user_auth as user_client
from utils import results

url=config.AUTH_DOMAIN

def create_admin_account(admin_email: str, admin_password: str):
    params = {"admin_email": admin_email, "admin_password": admin_password}
    r = httpx.post(url +'/admin/new_account/', params = params)
    #print(r.content)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def change_admin_password(admin_email: str):
    params = {"admin_email": admin_email}
    r = httpx.post(url +'/admin/change_password/', params = params)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def admin_login(admin_email: str, admin_password: str, return_tokens = False):
    params = {"admin_email": admin_email, "admin_password": admin_password}
    r = httpx.post(url +'/admin/login/password/', params = params)
    try:
        login_result = orjson.loads(r.content) 
        login_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))
    
    if return_tokens and r.status_code == httpx.codes.OK:
        admin_refresh_token = login_result["data"]["admin_refresh_token"]
        return admin_refresh_token
    else:
        return login_result 

def get_admin_session(admin_refresh_token: str, return_tokens = False): 
    params = {"admin_refresh_token": admin_refresh_token}
    r = httpx.post(url +'/admin/login/session/', params = params)
    try:
        session_result = orjson.loads(r.content)
        session_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))
    #print(session_result) #debugging
    if return_tokens and r.status_code == httpx.codes.OK:
        admin_user_id = session_result["data"]["admin_user_id"]
        admin_id_token = session_result["data"]["admin_id_token"]
        return admin_user_id, admin_id_token
    else:
        return session_result 

def verify_admin_session(admin_user_id: str, admin_id_token: str):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token}
    r = httpx.post(url +'/admin/verify_session/', params = params)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def create_user_group(admin_user_id: str, admin_id_token: str, new_group_name: str, group_user_params: Dict[str, Any] = {}):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "new_group_name": new_group_name, "group_user_params" : orjson.dumps(group_user_params) }
    r = httpx.post(url +'/admin/create_user_group/', params = params)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def get_admins_groups(admin_user_id: str, admin_id_token: str, return_list = False):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token}
    r = httpx.get(url +'/admin/get_user_groups/', params = params)
    try:
        result = orjson.loads(r.content)
        result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))
    
    if return_list and r.status_code == httpx.codes.OK:
        groups = result["data"]["groups"]
        return groups 
    else:
        return result 

def get_group_users(admin_user_id: str, admin_id_token: str, group_name: str, return_list = False):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "group_name": group_name}
    r = httpx.get(url +'/admin/get_group_users/', params = params)
    try:
        result = orjson.loads(r.content)
        result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))
    
    if return_list and r.status_code == httpx.codes.OK:
        users = result["data"]["users"]
        return users 
    else:
        return result 

def get_user_id_by_email(user_email: str, admin_user_id: str, admin_id_token: str, group_name: str):
    params = {"user_email": user_email, "admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "group_name": group_name}
    r = httpx.get(url +'/admin/get_uid_by_email/', params = params)
    try:
        user_id_result = orjson.loads(r.content)
        user_id_result.update({"url": str(r.url)})
        #print(user_id_result)
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 
    return user_id_result

def get_user_email(user_id: str, admin_user_id: str, admin_id_token: str, group_name: str):
    params = {"user_id": user_id, "admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "group_name": group_name}
    r = httpx.get(url +'/admin/get_email_by_uid/', params = params)
    try:
        user_email_result = orjson.loads(r.content)
        user_email_result.update({"url": str(r.url)})
        #print(user_email_result)
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 
    return user_email_result

def read_user_metadata(admin_user_id: str, admin_id_token: str, user_id: str, group: str):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "user_id": user_id, "group": group}
    r = httpx.get(url +'/admin/read_user_metadata/', params = params)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def write_user_metadata(admin_user_id: str, admin_id_token: str, user_id: str, group: str, dictionary: Dict[str, Any]): #all dicts passed to fastapi over HTTP must be string representations
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "user_id": user_id, "group": group, "dictionary": orjson.dumps(dictionary)}
    r = httpx.post(url +'/admin/write_user_metadata/', params = params)
    #print(r)
    #print(r.content)
    #print(r.url)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def reset_user(admin_user_id: str, admin_id_token: str, user_id: str, group_name: str):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "user_id": user_id, "group_name": group_name}
    r = httpx.post(url +'/admin/reset_user/', params=params)
    try:
        result = orjson.loads(r.content)
        result.update({"url": str(r.url)})
        return result
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def change_group_schema(admin_user_id: str, admin_id_token: str, group_name: str, new_schema_dict: Dict[str, Any], reset_all: bool):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "group_name": group_name, "new_schema_dict": orjson.dumps(new_schema_dict), "reset_all": reset_all}
    r = httpx.post(url +'/admin/change_group_schema/', params = params)
    #print(r)
    #print(r.content)
    #print(r.url)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def admin_delete_user(admin_user_id: str, admin_id_token: str, user_id: str, group_name: str):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "user_id": user_id, "group_name": group_name}
    r = httpx.delete(url +'/admin/delete_user/', params = params)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def delete_group(admin_user_id: str,admin_id_token: str, group_name: str):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "group_name": group_name}
    r = httpx.delete(url +'/admin/delete_group/', params = params)
    print(r)
    print(r.content)
    print(r.url)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def delete_admin_account(admin_email: str, admin_password: str):
    params = {"admin_email": admin_email, "admin_password": admin_password}
    r = httpx.delete(url +'/admin/delete_admin_account/', params = params)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

if __name__ == "__main__":
    print("This is a Unit Test: Oasis-Auth User Client")
	
    admin_pass = input("Enter the admin password to start the test: ")

	#print(sys.argv)
    if len(sys.argv) < 2:
        print("Please specify one of the following tests as a command line argument:")
        tests = ["test_create","test_changepass","test_login","test_revoke","test_delete"]
        for test in tests:
            print(test)
        print("Example: python3 firebase_utils.py test_login")
        sys.exit()

    #Should run the code to deal with an existing admin/user in the system
    if sys.argv[1] == "test_create":
        print(create_admin_account(admin_email="hello@oasis-x.io", admin_password=admin_pass))
    
    if sys.argv[1] == "test_changepass":
        print(change_admin_password(admin_email="hello@oasis-x.io"))

    #before running this create a new user & password in the oasis-users group using the user_client testing interface
    if sys.argv[1] == "test_authentication":
        print("Testing admin login w/ username & password...")
        admin_refresh_token = admin_login(admin_email="hello@oasis-x.io", admin_password=admin_pass, return_tokens=True)
        print("Success.")
        print("Testing retreival of admin session w/ refresh token...")
        admin_user_id, admin_id_token = get_admin_session(admin_refresh_token, return_tokens=True) #return tokens to upack the response data into a tuple
        print("Success")
        print("Testing verification of admin session w/ local credentials...")
        print(verify_admin_session(admin_user_id, admin_id_token))
        print("Success")

        user_email = "leemichael289@gmail.com"#input("Provide a test-user email address: ")
        user_pass = "insecurepassword"#input("Provide a test-user password: ")
        print(user_client.password_login(email=user_email, password=user_pass, admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2", group_name="oasis-users"))
        user_token = user_client.password_login(email=user_email, password=user_pass, admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2", group_name="oasis-users", return_tokens=True)
        user_id, id_token = user_client.get_session(user_token, admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2", group_name="oasis-users", return_tokens=True)

        print("Testing read & write:")
        #Should succeed and return a user object
        print(read_user_metadata(admin_user_id, admin_id_token, user_id, "oasis-users"))
        #Should succeed and return a write result for default oasis values
        print(write_user_metadata(admin_user_id, admin_id_token, user_id, group= "oasis-users", dictionary= {"current_plan_last_billing": datetime.now()}))
   
    #Delete the user you made for the above tests
    if sys.argv[1] == "test_delete_user":
        from utils import firebase

        print("Testing admin login w/ username & password...")
        admin_refresh_token = admin_login(admin_email="hello@oasis-x.io", admin_password=admin_pass, return_tokens=True)
        print("Success.")
        print("Testing retreival of admin session w/ refresh token...")
        admin_user_id, admin_id_token = get_admin_session(admin_refresh_token, return_tokens=True)
        print("Success")
        print("Testing admin create & delete password...")
        user_email = input("Provide a test-user email address: ")
        user = firebase.admin_auth.get_user_by_email(user_email) #We now expose our own endpoint for this
        print(admin_delete_user(admin_user_id, admin_id_token, user.uid, "oasis-users"))
    
    #create and delete a group with additional parameters
    if sys.argv[1] == "test_create_delete_group":
        print("Testing admin login w/ username & password...")
        admin_refresh_token = admin_login(admin_email="hello@oasis-x.io", admin_password=admin_pass, return_tokens=True)
        print("Success.")
        print("Testing retreival of admin session w/ refresh token...")
        admin_user_id, admin_id_token = get_admin_session(admin_refresh_token, return_tokens=True)
        print("Success")
        print("Testing group creation...")
        print(create_user_group(admin_user_id, admin_id_token, "test-group", {"Doe": "A deer, a female deer", "Ray": "A pocket full of sun"}))
        time.sleep(3)

        print("Admin Groups:" + str(get_admins_groups(admin_user_id, admin_id_token, return_list=True)))
        print("Test group's users:" + str(get_group_users(admin_user_id, admin_id_token, "test-group", return_list=True)))

        print("Testing group deletion...")
        print(delete_group(admin_user_id, admin_id_token, "test-group"))

    #create and delete a dummy admin. You can upgrade the existing account if you have not previously deleted the user
    if sys.argv[1] == "test_create_delete_admin":
        
        admin_user_email = input("Provide a working test-user email: ")
        admin_user_pass = input("Provide a working test-user password: ")

        print("Testing admin creation...")
        print(create_admin_account(admin_user_email, admin_user_pass))

        print("Testing admin login w/ username & password...")
        admin_refresh_token = admin_login(admin_email=admin_user_email, admin_password=admin_user_pass, return_tokens=True)
        print("Success.")
        print("Testing retreival of admin session w/ refresh token...")
        admin_user_id, admin_id_token = get_admin_session(admin_refresh_token, return_tokens=True)
        print("Success")
        print("Testing group creation...")
        print(create_user_group(admin_user_id, admin_id_token, "test-group", {"Doe": "A deer, a female deer", "Ray": "A pocket full of sun"}))

        print("Testing writes.")
        #print(user_client.create_new_user("mike@oasis-x.io", "notpassword", admin_user_id, "test-group"))
        #time.sleep(60)
        refresh_token = user_client.password_login("mike@oasis-x.io", "notpassword", admin_user_id, "test-group", return_tokens=True)
        print(refresh_token)
        user_id, id_token = user_client.get_session(refresh_token, admin_user_id, "test-group", return_tokens=True)
        #should work
        print(write_user_metadata(admin_user_id, admin_id_token, user_id, "test-group", {"Ray": "just a really cool guy, I guess"}))
        #should fail, because you cannot overwrite the default oasis configs
        print(write_user_metadata(admin_user_id, admin_id_token, user_id, "test-group", {"current_plan_last_billing": datetime.now()}))
        
        #should succeed in updating the test-group schema, preserving all oasis-x values and adding 1 new field
        print(change_group_schema(admin_user_id, admin_id_token, "test-group", {"Doe": "A deer, a female deer", 
                                                                                "Ray": "A pocket full of sun",
                                                                                "Me": "A name I call myself"}, reset_all=False))

        #should reset the user's data into the new schema, with default values given 
        print(reset_user(admin_user_id, admin_id_token, user_id, "test-group"))

        print("Testing admin deletion...") #should take the created test-group with it
        print(delete_admin_account(admin_user_email, admin_user_pass))

    if sys.argv[1] == "test_get_info":
        admin_refresh_token = admin_login(admin_email="hello@oasis-x.io", admin_password=admin_pass, return_tokens=True)
        print("Success.")
        print("Testing retreival of admin session w/ refresh token...")
        admin_user_id, admin_id_token = get_admin_session(admin_refresh_token, return_tokens=True)
        
        user_email = "leemichael289@gmail.com"

        print("Testing get_user_id_by_email...")
        result = get_user_id_by_email(user_email, admin_user_id, admin_id_token, "oasis-users")
        user_id = result["data"]["user_id"]
        print("User-Identifying String:" + user_id)

        print("Testing get user email...")
        result = get_user_email(user_id, admin_user_id, admin_id_token, "oasis-users")
        user_email = result["data"]["user_email"]
        print("User Email:" + user_email)

