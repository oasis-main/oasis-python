import requests
import stripe

# import shell modules
import sys
import os

# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
pwd = os.getcwd()

sys.path.append(pwd)

import keys

stripe.api_key = keys.STRIPE_PRIVATE

#Price and product functions

def list_prices():
    response = stripe.Price.list(
        expand=['data.product']
    )
    return response

def create_product(unit_amount: int, name: str, description: str, interval: str):
    #unit_amount is the price of the product in whatever currency is specified
    #interval is the frequency of charges for a subscription product
    #   options: day, week, month, year
    #lookup key is a string used as an identifier for searching
    response = stripe.Product.create(
        name=name,
        description=description,
        default_price_data={
            "unit_amount": unit_amount,
            "currency": "usd",
            "recurring": {"interval": interval},
        },
        expand=["default_price"],
    )
    return response

def list_products():
    response = stripe.Product.list(
        expand=['data.price']
    )
    return response

#Customer functions
def create_customer(oasis_x_id: str, email_addr: str, name: str):
    return stripe.Customer.create(
        email=email_addr,
        name=name,
        metadata={
            #Double link with oasis-x id
            'oasis_x_id': oasis_x_id
        }
    )

def get_customer_by_oasis_x_id(oasis_x_id: str):
    return stripe.Customer.search(
        query='metadata["oasis_x_id"]: oasis_x_id'
    )

def list_customers():
    return stripe.Customer.list()

#Subscription functions

# This function probably should not be used, as our app's subscriptions are 
# presently created by the create_checkout_session function
    # def create_subscription(customer_id: str, price_id: str, quantity: int):
    #     subscription = stripe.Subscription.create(
    #         customer=customer_id,
    #         line_items=[
    #             {
    #                 'price': price_id,
    #                 'quantity': quantity
    #             }
    #         ],
    #         payment_behavior='default_incomplete',
    #         expand=['latest_invoice.payment_intent'],
    #     )

def list_subscriptions(customer_id: str):
    try:
        # Cancel the subscription by deleting it
        subscriptions = stripe.Subscription.list(
            customer=customer_id,
            status='all',
            expand=['data.default_payment_method']
        )
        return jsonify(subscriptions=subscriptions)
    except Exception as e:
        return jsonify(error=str(e)), 403


def cancel_subscription(subscription_id: str):
    try:
        # Cancel the subscription by deleting it
        deletedSubscription = stripe.Subscription.delete(data['subscription_id'])
        return jsonify(subscription=deletedSubscription)
    except Exception as e:
        return jsonify(error=str(e)), 403

#Customer portal
def create_customer_portal(customer, return_url):
    portalSession = stripe.billing_portal.Session.create(
        customer=customer,
        return_url=return_url,
    )
    return redirect(portalSession.url, code=303)

#Checkout session functions
def create_checkout_session(price_id: str, quantity: int, mode: str, success_url: str, cancel_url: str):
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            #This object is VERY picky with formatting
            #Must be passed in a way that gets to Stripe in the following format:
              # "line_items": {
              #   "0": {
              #     "quantity": "1",
              #     "price": "price_1MPA7DCwHfTd1Q1I4drOsYFM"
              #   }
              # },
            #This may be easy to ensure, but I had a tough time with it when trying to define the line_items object via
            #a function
            line_items=[
                {
                    'price': price_id,
                    'quantity': quantity
                }
            ],
            mode="subscription",
        )
        return checkout_session
    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught

        print('Status is: %s' % e.http_status)
        print('Code is: %s' % e.code)
        # param is '' in this case
        print('Param is: %s' % e.param)
        print('Message is: %s' % e.user_message)
    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        pass
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        print(f'Invalid request:{e}')
        pass
    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        pass
    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        pass
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        pass
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        print(f'Exception:{e}')
        pass


#Webhooks
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

#Not yet used
def create_account(oasis_x_id: str, email_addr: str):
    return stripe.Account.create(
        # options are custom, express, and standard - we want standard at this time
        type="standard",
        # default is our company's country. Probably want to start with US or US and Canada. Formatted as ISO 3166-1 alpha-2 country code
        country="US",
        email=email_addr,
        metadata={
            # I think we probably want to double-link with our oasis-x user object, but we obviously don't have to if we're doing a SQL-style data structure
            'oasis_x_id': oasis_x_id
        }
    )
    # This function returns a response
    # response.id
    # store on oasis_x_user object as stripe_account_id (or other appropriate name) - this will be used to query their account info when needed

def get_account_by_stripe_account_id(stripe_account_id: str):
    return Stripe.Account.retrieve(stripe_account_id)

def create_account_link(stripe_account_id: str):
    return stripe.AccountLink.create(
        # account is the account id of the stripe account which is to be authenticated and linked
        account=stripe_account_id,
        # refresh_url is required, and is where user is directed if the account link has expired (relatively unlikely scenario)
        # refresh_url should be a page you will need to create which basically calls this send_account_link function again to create a new account link request
        refresh_url="https://example.com/reauth",
        # return_url is where the user should be directed when they are "returned" after account link has been clicked and validated
        return_url="https://example.com/return",
        # type should always be account_onboarding for our purposes
        type="account_onboarding",
    )
    # this function returns a response
    # after account_link is created, direct user to response.url
    # when the user navigates to response.url, their account will be linked, and they will be returned to return_url (perhaps after a click)

def create_payment_intent(amount: float):
    return stripe.PaymentIntent.create(
        # I believe that the {{CONNECTED_STRIPE_ACCOUNT_ID}} grabs the value from the stripe module but I'm not 100% sure
        stripe_account='{{CONNECTED_STRIPE_ACCOUNT_ID}}',
        amount=amount,
        # currency is a three-letter ISO currency code, in lowercase. Must be a supported currency.
        currency='usd',
        # payment_method_types can include any of these methods:
        # acss_debit, affirm, afterpay_clearpay, alipay, au_becs_debit, bacs_debit, bancontact, blik, boleto, card, card_present, customer_balance, eps, fpx, giropay, grabpay, ideal, interac_present, klarna, konbini, link, oxxo, p24, paynow, pix, promptpay, sepa_debit, sofort, us_bank_account, and wechat_pay.
        payment_method_types=["card"],
        # Stripe automatically includes stripe_account_id since AccountLink has been created and clicked
        # payee is not yet specified - Stripe is just creating an intention to send a payment
        # The PaymentIntent object's purpose is to initiate the process of entering required information for the payment, entering payment info, etc.
        # this function returns a response
        # response.client_secret is can be accessed with a publishable key, and is used to complete the payment after payment method has been validated and such
    )

