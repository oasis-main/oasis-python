#handles oasis-authentication
from fastapi import FastAPI
import sys
import os
from typing import Dict
# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
pwd = os.getcwd()
sys.path.append(pwd)

import stripe
import stripe_api
import keys
# This is your test secret API key.
stripe.api_key = keys.STRIPE_PRIVATE

app = FastAPI()

@app.get("/")
async def welcome():
    return {
        "Stripe Demo"
    }

#Checkout endpoints

@app.post('/checkout/create')
def create_checkout_session(price_id: str, quantity: int, mode: str, success_url: str, cancel_url: str):
    checkout_session = stripe_api.create_checkout_session(price_id, quantity, mode, success_url, cancel_url)
    print(f'checkout_session:{checkout_session}')
    return checkout_session

#Account endpoints

@app.post('/account/create')
def create_account(oasis_x_id: str, email_addr: str):
    new_account = stripe_api.create_account(oasis_x_id, email_addr)
    new_account_link = stripe_api.create_account_link(new_account.id)
    return new_account_link.url

@app.get('/account/get')
def get_account(stripe_account_id: str):
    return stripe_api.get_account_by_stripe_account_id(stripe_account_id)

#Customer endpoints
@app.post('/customer/create')
def create_customer(oasis_x_id: str, email_addr: str, name: str):
    return stripe_api.create_customer(oasis_x_id, email_addr, name)

@app.get('/customer/list')
def list_customers():
    return stripe_api.list_customers()

@app.get('/customer/get')
def get_customer_by_oasis_x_id(oasis_x_id: str):
    return stripe_api.get_customer_by_oasis_x_id(oasis_x_id)

#Price and product endpoints

@app.post('/product/create')
def create_product(unit_amount: int, name: str, description: str, interval: str):
    #unit_amount is the price of the product in whatever currency is specified
    #   unit_amount is best specified in cents
    #interval is the frequency of charges for a subscription product
    #   options: day, week, month, year
    return stripe_api.create_product(unit_amount, name, description, interval)

# @app.get('/product/list')
# def list_products():
#     return stripe_api.get_products()

@app.get('/price/list')
def list_prices():
    return stripe_api.list_prices()

#Subscription endpoints
#Note that creating subscriptions is handled by the create_checkout_session function, so
#no create endpoint is provided here, though code to do so exists in stripe_api.py

@app.get('/subscription/list')
def list_subscriptions(customer_id: str):
    return stripe_api.list_subscriptions(customer_id)


@app.delete('/subscription/cancel')
#Cancel = delete, as delete method is used, but wording as 'cancel' feels appropriate - can be changed later
def cancel_subscription(subscription_id: str):
    return stripe_api.cancel_subscription(subscription_id)

#Portal session endpoint
@app.post('/portal-session/create')
def create_customer_portal():
    return stripe_api.create_customer_portal()

#Webhook endpoint
@app.post('/webhook')
def webhook_received():
    # Replace this endpoint secret with your endpoint's unique secret
    # If you are testing with the CLI, find the secret by running 'stripe listen'
    # If you are using an endpoint defined with the API or dashboard, look in your webhook settings
    # at https://dashboard.stripe.com/webhooks
    webhook_secret = 'whsec_12345'
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    print('event ' + event_type)

    if event_type == 'checkout.session.completed':
        print('🔔 Payment succeeded!')
    elif event_type == 'customer.subscription.trial_will_end':
        print('Subscription trial will end')
    elif event_type == 'customer.subscription.created':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.updated':
        print('Subscription created %s', event.id)
    elif event_type == 'customer.subscription.deleted':
        # handle subscription canceled automatically based
        # upon your subscription settings. Or if the user cancels it.
        print('Subscription canceled: %s', event.id)

    return jsonify({'status': 'success'})