import sys
import json
import httpx
import orjson

# import shell modules
import sys

import config
import config
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)
from utils import results

server_uri = config.MARKETS_DOMAIN

#User/auth functions
def create_new_user(email: str, password: str):
    params = {"email": email, "password": password}
    r = httpx.post(server_uri +'/user/create_account/', params = params)
    try:
        attempt_result = orjson.loads(r.content) #we're going to have to parse this into a return json for each one
        attempt_result.update({"url": str(r.url)})
        return attempt_result # The name of the return variable should tell us how to parse the resulting dictionary 
    except:
        return results.response(attempt=False,allowed=False,message=r.message, url=str(r.url)) 

def password_login(email: str, password: str):
    params = {"email": email, "password": password}
    r = httpx.post(server_uri +'/user/login/password/' , params = params)
    try:
        login_result = orjson.loads(r.content)
        login_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return login_result # The name of the return variable should tell us how to parse the resulting dictionary

def get_user_id_by_email(email: str):
    params = {"email": email}
    r = httpx.get(server_uri + '/user/get/id/', params = params)
    try:
        attempt_result = orjson.loads(r.content)
        attempt_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return attempt_result # The name of the return variable should tell us how to parse the resulting dictionary

#Stripe functions
def create_stripe_account(email: str, oasis_x_id: str):
    params = {"email": email, "oasis_x_id": oasis_x_id}
    r = httpx.post(server_uri + '/account/create/', params = params, timeout=10.0)
    print(f"create_stripe_account r: {r}")
    try:
        attempt_result = orjson.loads(r.content)
        #  Response from account creation server includes a url field to
        #  direct user to complete account creation on Stripe, so this must
        #  be stored in a separate field
        attempt_result.update({"redirect_url": attempt_result["url"]})
        attempt_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return attempt_result

#General functions
def create_line_item(price: str, quantity: int = 1):
    return [
        {
            "price": price,
            "quantity": quantity
        }
    ]

#Product functions
def create_product(unit_amount: float, name: str, description: str, interval: str):
    path = server_uri + '/product/create/'
    params = {
        'unit_amount': unit_amount,
        'name': name,
        'description': description,
        'interval': interval
    }
    response = httpx.post(path, params = params)
    attempt_result = json.loads(response.text)
    data = attempt_result.get('data')
    return data

def list_products():
    path = server_uri + '/product/list/'
    response = httpx.get(path)
    attempt_result = json.loads(response.text)
    data = attempt_result.get('data')
    return data

#Price functions
def list_prices():
    path = server_uri + '/price/list/'
    response = httpx.get(path)
    attempt_result = json.loads(response.text)
    data = attempt_result.get('data')
    return data

#Customer functions

def list_customers():
    path = server_uri + '/customer/list/'
    response = httpx.get(path)
    attempt_result = json.loads(response.text)
    data = attempt_result.get('data')
    return data

def create_customer(oasis_x_id: str, email_addr: str, name: str):
    path = server_uri + '/customer/create/'
    params = {
        'email_addr': email_addr,
        'oasis_x_id': oasis_x_id,
        'name': name
    }
    response = httpx.post(path, params = params)
    attempt_result = json.loads(response.text)
    data = attempt_result.get('data')
    return data

#Subscription functions
def list_subscriptions(customer_id: str):
    path = server_uri + '/subscription/list/'
    response = httpx.get(path)
    attempt_result = json.loads(response.text)
    data = attempt_result.get('data')
    return data

#Checkout functions
def create_checkout_session(price_id: str, quantity: int, mode: str, success_url: str, cancel_url: str):
    path = server_uri + '/checkout/create/'
    params = {'price_id': price_id, 'quantity': quantity, 'mode': mode, 'success_url': success_url, 'cancel_url': cancel_url }
    r = httpx.post(path, params = params)
    attempt_result = json.loads(r.text) #we're going to have to parse this into a return json for each one
    return attempt_result

