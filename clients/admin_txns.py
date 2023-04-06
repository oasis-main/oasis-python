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

from typing import Dict, Any

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
    r = httpx.post(server_uri +'/user/password_login/' , params = params)
    try:
        login_result = orjson.loads(r.content)
        login_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return login_result

def create_user_session(refresh_token: str):
    path = server_uri + '/user/create_session/'
    data = {"refresh_token": refresh_token}
    r = httpx.post(path, json = data)
    try:
        session_result = orjson.loads(r.content)
        session_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return session_result

def verify_user_session(user_id: str, id_token: str):
    path = server_uri + '/user/create_session/'
    json_body = {"refresh_token": refresh_token}
    r = httpx.post(path, json = json_body)
    try:
        verify_result = orjson.loads(r.content)
        verify_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return verify_result

def get_user_id_by_email(email: str):
    params = {"email": email}
    r = httpx.get(server_uri + '/user/get_id_by_email/', params = params)
    try:
        attempt_result = orjson.loads(r.content)
        attempt_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return attempt_result

def read_user_metadata(oasis_x_id: str):
    params = {"user_id": oasis_x_id}
    r = httpx.get(server_uri + '/user/read_metadata/', params = params)
    try:
        attempt_result = orjson.loads(r.content)
        attempt_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return attempt_result

def write_user_metadata(oasis_x_id: str, metadata: Dict[str, Any]):
    path = server_uri + '/user/write_metadata/'
    body = {"user_id": oasis_x_id, "metadata": str(orjson.dumps(metadata), encoding="utf-8")}
    print(f"write_user_metadata body: {body}")
    r = httpx.post(path, json = body)
    try:
        attempt_result = orjson.loads(r.content)
        attempt_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return attempt_result

#Customer functions
def list_customers():
    path = server_uri + '/customer/list/'
    r = httpx.get(path)
    attempt_result = orjson.loads(r.text)
    data = attempt_result.get('data')
    return data

def get_customer_by_stripe_id(stripe_customer_id: str):
    params = {"stripe_customer_id": stripe_customer_id}
    r = httpx.get(server_uri + '/customer/get_by_stripe_id/', params = params)
    try:
        attempt_result = orjson.loads(r.content)
        attempt_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return attempt_result

def create_customer(oasis_x_id: str, email: str, name: str):
    path = server_uri + '/customer/create/'
    params = {
        'email': email,
        'oasis_x_id': oasis_x_id,
        'name': name
    }
    r = httpx.post(path, params = params)
    print(f"create_customer_response: {r}")
    try:
        attempt_result = orjson.loads(r.content)
        attempt_result.update({"url": str(r.url)})
    except:
        return results.response(attempt=False,allowed=False,message=r.message,url=str(r.url)) 
    return attempt_result

#Reseller functions
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
    attempt_result = orjson.loads(response.text)
    data = attempt_result.get('data')
    return data

def list_products():
    path = server_uri + '/product/list/'
    response = httpx.get(path)
    attempt_result = orjson.loads(response.text)
    data = attempt_result.get('data')
    return data

#Price functions
def list_prices():
    path = server_uri + '/price/list/'
    response = httpx.get(path)
    attempt_result = orjson.loads(response.text)
    data = attempt_result.get('data')
    return data

#Subscription functions
def list_customer_subscriptions(customer_id: str):
    path = server_uri + '/subscription/list/'
    response = httpx.get(path)
    attempt_result = orjson.loads(response.text)
    data = attempt_result.get('data')
    return data

def create_subscription(user_id: str, id_token: str, price_id: str, success_url: str, cancel_url: str):
    #No dedicated create_subscription endpoint yet, though we could create one if necessary
    path = server_uri + '/checkout/create/'
    json_body = { 'price_id': price_id, 'quantity': 1, 'mode': "subscription", 'success_url': success_url, 'cancel_url': cancel_url }
    r = httpx.post(path, json = json_body)
    attempt_result = orjson.loads(r.text)
    data = attempt_result.get('data')
    return data

#Checkout functions
def create_checkout_session(user_id: str, id_token: str, price_id: str, quantity: int, mode: str, success_url: str, cancel_url: str):
    path = server_uri + '/checkout/create/'
    json_body = {'user_id': user_id, 'id_token': id_token, 'price_id': price_id, 'quantity': quantity, 'mode': mode, 'success_url': success_url, 'cancel_url': cancel_url }
    r = httpx.post(path, json = json_body)
    attempt_result = orjson.loads(r.text)
    data = attempt_result.get('data')
    return data

