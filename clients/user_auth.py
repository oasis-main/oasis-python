#user client code for accessing the API
import os
import sys
import orjson
import httpx

cwd = os.getcwd()
sys.path.append(cwd)
import config
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)

from utils import results
from typing import Literal, Optional

url=config.URL

def create_new_user(email: str, password: str, admin_user_id: str, group_name: str):
    params = {"email": email, "password": password, "admin_user_id": admin_user_id, "group_name": group_name}
    r = httpx.post(url +'/user/create_account/', params = params)
    #print(r.content)
    try:
        attempt_result = orjson.loads(r.content) #we're going to have to parse this into a return json for each one
        attempt_result.update({"url": str(r.url)})
        return attempt_result # The name of the return variable should tell us how to parse the resulting dictionary 
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object", url=str(r.url)) 

def change_password(email: str, admin_user_id: str, group_name: str):
    params = {"email": email, "admin_user_id": admin_user_id, "group_name": group_name}
    r = httpx.post(url +'/user/change_password/' , params = params)
    try:
        attempt_result = orjson.loads(r.content)
        attempt_result.update({"url": str(r.url)})
        return attempt_result # The name of the return variable should tell us how to parse the resulting dictionary 
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 

def password_login(email: str, password: str, admin_user_id: str, group_name: str, return_tokens = False):
    params = {"email": email, "password": password, "admin_user_id": admin_user_id, "group_name": group_name}
    r = httpx.post(url +'/user/login/password/' , params = params)
    try:
        login_result = orjson.loads(r.content)
        login_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 
    
    if return_tokens and r.status_code == httpx.codes.OK:
        refresh_token = login_result["data"]["refresh_token"]
        return refresh_token
    else:
        return login_result # The name of the return variable should tell us how to parse the resulting dictionary

def get_session(refresh_token: str, admin_user_id: str, group_name: str, return_tokens = False):
    params = {"refresh_token": refresh_token, "admin_user_id": admin_user_id, "group_name": group_name}
    r = httpx.post(url +'/user/login/session/', params = params)
    try:
        session_result = orjson.loads(r.content)
        session_result.update({"url": str(r.url)})
        #print(session_result)
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 
    
    if return_tokens and r.status_code == httpx.codes.OK:
        user_id = session_result["data"]["user_id"]
        id_token = session_result["data"]["id_token"]
        return user_id, id_token
    else:
        return session_result # The name of the return variable should tell us how to parse the resulting dictionary

def verify_session(user_id: str, id_token: str, admin_user_id: str, group_name: str):
    params = {"user_id": user_id, "id_token": id_token, "admin_user_id": admin_user_id, "group_name": group_name}
    r = httpx.post(url +'/user/verify_session/' , params = params)
    try:
        allowed_result = orjson.loads(r.content)
        allowed_result.update({"url": str(r.url)})
        return allowed_result # The name of the return variable should tell us how to parse the resulting dictionary
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 

def request_user_access(user_id: str, id_token: str, admin_user_id: str, group: str, data_type: Literal["allowance_count","credit_balance","clearance_code"], field: str, required: str, emissions_kg: Optional[float] = 0.0000, check_only: Optional[bool] = False):
    params = {"user_id": user_id, "id_token": id_token, "admin_user_id": admin_user_id, "group": group, "data_type": data_type, "field": field, "required": required, "emissions_kg": emissions_kg, "check_only": check_only}
    r = httpx.post(url +'/user/access_request/', params = params)
    try:
        result = orjson.loads(r.content) 
        result.update({"url": str(r.url)})
        return result 
    except:
        return results.response(attempt=False, allowed=False, message = "Could not orjson.loads the response object",url=str(r.url))

def get_id_from_email(user_email: str, id_token: str, admin_user_id: str, group_name: str):
    params = {"user_email": user_email, "id_token": id_token, "admin_user_id": admin_user_id, "group_name": group_name}
    r = httpx.get(url +'/user/get_uid_by_email/', params = params)
    try:
        user_id_result = orjson.loads(r.content)
        user_id_result.update({"url": str(r.url)})
        #print(user_id_result)
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 
    
    return user_id_result

def get_email_from_id(user_id: str, id_token: str, admin_user_id: str, group_name: str):
    params = {"user_id": user_id, "id_token": id_token, "admin_user_id": admin_user_id, "group_name": group_name}
    r = httpx.get(url +'/user/get_email_by_uid/', params = params)
    try:
        user_email_result = orjson.loads(r.content)
        user_email_result.update({"url": str(r.url)})
        #print(user_email_result)
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 
    
    return user_email_result

def delete_user(user_id: str, password: str, admin_user_id: str, group_name: str):
    params = {"user_id": user_id, "password": password, "admin_user_id": admin_user_id, "group_name": group_name}
    r = httpx.delete(url +'/user/delete_account/' , params = params)
    try:
        attempt_result = orjson.loads(r.content)
        attempt_result.update({"url": str(r.url)})
        return attempt_result # The name of the return variable should tell us how to parse the resulting dictionary
    except:
        return results.response(attempt=False,allowed=False,message="Could not orjson.loads the response object",url=str(r.url)) 


if __name__ == "__main__":
    print("This is a Unit Test: Oasis-Auth User Client")
	
    admin_user_id="N3rLUQG4CQNxRNKZ3cBLN8Wli4v2"
	
    #print(sys.argv)
    if len(sys.argv) < 2:
        print("Please specify one of the following tests as a command line argument:")
        tests = ["test_create","test_changepass","test_login","test_revoke","test_delete"]
        for test in tests:
            print(test)
        print("Example: python3 firebase_utils.py test_login")
        sys.exit()

    if sys.argv[1] == "test_create":

        print("Creating a new user...")
        result = create_new_user("leemichael289@gmail.com", "insecurepassword", admin_user_id, "oasis-users") #requires verification before proceeding
        print(result)
	
    if sys.argv[1] == "test_changepass":
        print("Changing password...")
        result = change_password("leemichael289@gmail.com", admin_user_id, "oasis-users")
        print(result)

    if sys.argv[1] == "test_login":
        print("Logging-in with username & password...")
        result = password_login("leemichael289@gmail.com", "insecurepassword", admin_user_id, "oasis-users")
        refresh_token = result["data"]["refresh_token"]
        print("Refresh Token:" + refresh_token)

        print("Testing refresh token...")
        result = get_session(refresh_token, admin_user_id, "oasis-users")
        user_id = result["data"]["user_id"]
        id_token = result["data"]["id_token"]
        print("User-Identifying String:" + user_id)
        print("Temporary Access Token:" + id_token)

        print("Checking id_token status...")
        result = verify_session(user_id, id_token, admin_user_id, "oasis-users")
        print(result)
    
    if sys.argv[1] == "test_delete":
        print("Logging-in with username & password...")
        refresh_token = password_login("leemichael289@gmail.com", "insecurepassword", admin_user_id, "oasis-users", return_tokens=True)
        
        print("Getting local credentials for test...")
        user_id, id_token = get_session(refresh_token, admin_user_id, "oasis-users", return_tokens=True)
        print(id_token)
        print(user_id)

        print("Checking id_token status...")
        result = verify_session(user_id, id_token, admin_user_id, "oasis-users")
        print(result)

        print("Deleting user...")
        result = delete_user(user_id, "insecurepassword", admin_user_id, "oasis-users")
        print(result)

        print("Checking old id_token status...")
        result = verify_session(user_id, id_token, admin_user_id, "oasis-users")
        print(result)

        print("Logging-in with deleted username & password...")
        refresh_token = password_login("leemichael289@gmail.com", "insecurepassword", admin_user_id, "oasis-users")

    if sys.argv[1] == "test_access_request":
        print("Testing user access allowances...")
        user_email = "leemichael289@gmail.com"#input("Provide a test-user email address: ")
        user_pass = "insecurepassword"#input("Provide a test-user password: ")
        print(password_login(email=user_email, password=user_pass, admin_user_id=admin_user_id, group_name="oasis-users"))
        user_token = password_login(email=user_email, password=user_pass, admin_user_id=admin_user_id, group_name="oasis-users", return_tokens=True)
        print(get_session(user_token, admin_user_id=admin_user_id, group_name="oasis-users", return_tokens=True))
        user_id, id_token = get_session(user_token, admin_user_id=admin_user_id, group_name="oasis-users", return_tokens=True) 
        #Should succeed
        print(request_user_access(user_id, id_token, admin_user_id, group="oasis-users", data_type = "allowance_count", field = "new_devices_remaining", required = 1))
        #Should succeed
        print(request_user_access(user_id, id_token, admin_user_id, group="oasis-users", data_type = "credit_balance", field ="database_gb_usage_remaining", required = 0.01))
        #Should succeed
        print(request_user_access(user_id, id_token, admin_user_id, group="oasis-users", data_type = "clearance_code", field ="data_plan", required = "community"))
        #Should fail
        print(request_user_access(user_id, id_token, admin_user_id, group="oasis-users", data_type = "allowance_count", field ="knowledge_ai_training_tokens", required = 1, check_only=True))
        #Should fail
        print(request_user_access(user_id, id_token, admin_user_id, group="oasis-users", data_type = "credit_balance", field ="database_gb_usage_remaining", required = 1.00, check_only=True))
        #Should fail
        print(request_user_access(user_id, id_token, admin_user_id, group="oasis-users", data_type = "clearance_code", field ="data_plan", required = "standard"))

    if sys.argv[1] == "test_get_info":
        user_email = "leemichael289@gmail.com"#input("Provide a test-user email address: ")
        user_pass = "insecurepassword"#input("Provide a test-user password: ")
        print(password_login(email=user_email, password=user_pass, admin_user_id=admin_user_id, group_name="oasis-users"))
        user_token = password_login(email=user_email, password=user_pass, admin_user_id=admin_user_id, group_name="oasis-users", return_tokens=True)
        print(get_session(user_token, admin_user_id=admin_user_id, group_name="oasis-users", return_tokens=True))
        user_id, id_token = get_session(user_token, admin_user_id=admin_user_id, group_name="oasis-users", return_tokens=True) 
        
        print("Testing get_user_id_by_email...")
        result = get_id_from_email(user_email, id_token, admin_user_id, "oasis-users")
        user_id = result["data"]["user_id"]
        print("User-Identifying String:" + user_id)

        print("Testing get user email...")
        result = get_email_from_id(user_id, id_token, admin_user_id, "oasis-users")
        user_email = result["data"]["user_email"]
        print("User Email:" + user_email)