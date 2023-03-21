import sys
import json
import httpx

# import shell modules
import sys

import config
import config
PWD = config.OS_PATH + config.CWD
sys.path.append(PWD)

server_uri = config.MARKETS_DOMAIN

#User/account functions
def create_account(oasis_x_id: str, email_addr: str):
    path = server_uri + '/account/create/'
    params = {
        'oasis_x_id': oasis_x_id,
        'email_addr': email_addr
    }
    response = httpx.post(path, params = params)
    attempt_result = json.loads(response.text)
    data = attempt_result.get('data')
    return data

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

