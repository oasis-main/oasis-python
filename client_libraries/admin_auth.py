#Administrator account clients
#for managing groups of users
import time
import sys
import orjson
import httpx
from datetime import datetime

#OS_PATH = '/Users/Michaellee/Documents/Runes/oasis-x' #local
#OS_PATH = "/home/sean/code/oasis-x"
OS_PATH = "/home/ubuntu"
PWD = OS_PATH + '/oasis-auth'
sys.path.append(PWD)

from typing import Literal, Dict, Any

import user_auth
from utils import results

#Cloud URL
url = "https://auth.oasis-x.io"
#Local URL
#url = "http://localhost:8000"

def create_admin_account(admin_email: str, admin_password: str):
    params = {"admin_email": admin_email, "admin_password": admin_password}
    r = httpx.put(url +'/admin/new_account/', params = params)
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

def read_user_metadata(admin_user_id: str, admin_id_token: str, user_id: str, group: str):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "user_id": user_id, "group": group}
    r = httpx.get(url +'/admin/read_user/', params = params)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def write_user_metadata(admin_user_id: str, admin_id_token: str, user_id: str, group: str, dictionary: Dict[str, Any]): #all dicts passed to fastapi over HTTP must be string representations
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "user_id": user_id, "group": group, "dictionary": orjson.dumps(dictionary)}
    r = httpx.post(url +'/admin/write_user/', params = params)
    #print(r)
    #print(r.content)
    #print(r.url)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def request_user_access(admin_user_id: str, admin_id_token: str, user_id: str, group: str, data_type: Literal["allowance_count","credit_balance","clearance_code"], field: str, required: str, emissions_kg: float = 0.0000, check_only: bool = False):
    params = {"admin_user_id": admin_user_id, "admin_id_token": admin_id_token, "user_id": user_id, "group": group, "data_type": data_type, "field": field, "required": required, "emissions_kg": emissions_kg, "check_only": check_only}
    r = httpx.post(url +'/admin/user_access_request/', params = params)
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

    #before running this create a new user & password in the oasis-users group using the user_auth testing interface
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
        print("Testing user access allowances...")
        user_email = "leemichael289@gmail.com"#input("Provide a test-user email address: ")
        user_pass = "insecurepassword"#input("Provide a test-user password: ")
        print(user_auth.password_login(email=user_email, password=user_pass, admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2", group_name="oasis-users"))
        user_token = user_auth.password_login(email=user_email, password=user_pass, admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2", group_name="oasis-users", return_tokens=True)
        user_id, id_token = user_auth.get_session(user_token, admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2", group_name="oasis-users", return_tokens=True) 
        #Should succeed
        print(request_user_access(admin_user_id, admin_id_token, user_id, group="oasis-users", data_type = "allowance_count", field = "new_devices_remaining", required = 1))
        #Should succeed
        print(request_user_access(admin_user_id, admin_id_token, user_id, group="oasis-users", data_type = "credit_balance", field ="database_gb_usage_remaining", required = 0.01))
        #Should succeed
        print(request_user_access(admin_user_id, admin_id_token, user_id, group="oasis-users", data_type = "clearance_code", field ="data_plan", required = "community"))
        #Should fail
        print(request_user_access(admin_user_id, admin_id_token, user_id, group="oasis-users", data_type = "allowance_count", field ="knowledge_ai_training_tokens", required = 1, check_only=True))
        #Should fail
        print(request_user_access(admin_user_id, admin_id_token, user_id, group="oasis-users", data_type = "credit_balance", field ="database_gb_usage_remaining", required = 1.00, check_only=True))
        #Should fail
        print(request_user_access(admin_user_id, admin_id_token, user_id, group="oasis-users", data_type = "clearance_code", field ="data_plan", required = "standard"))
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
        user = firebase.admin_auth.get_user_by_email(user_email)
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
        #print(user_auth.create_new_user("mike@oasis-x.io", "notpassword", admin_user_id, "test-group"))
        #time.sleep(60)
        refresh_token = user_auth.password_login("mike@oasis-x.io", "notpassword", admin_user_id, "test-group", return_tokens=True)
        print(refresh_token)
        user_id, id_token = user_auth.get_session(refresh_token, admin_user_id, "test-group", return_tokens=True)
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