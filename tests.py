# Requirements:
#   Stripe account with Stripe Connect branding configured - requires credit card info to be uploaded (I think)
#   see https://stripe.com/docs/connect/standard-accounts#how-to-use-connect-onboarding-for-standard-accounts
# Configuration:
#   Create keys.py file in this folder(oasis-markets/api) and add stripe private key as STRIPE_PRIVATE

# import shell modules
import sys
import os

# Rather than manually specify these values on everyone's environment, it probaly makes sense to use a function to get the
# cwd/pwd/whatever we want to call it until the module has been integrated with the existing code base
pwd = os.getcwd()

# Set proper path for modules
sys.path.append(pwd)

# Import stripe package
import stripe

# Import library to be tested
import stripe_api


oasis_x_id = 'pat_carroll'
email_addr = 'patrick.w.carroll@gmail.com'

new_account = stripe_api.create_account(oasis_x_id, email_addr)

print(f'new_account:{new_account}')

# Function below will fail unless Stripe Connect branding has been configured
new_account_link = stripe_api.create_account_link(new_account.id)

print(f'new_account_link:{new_account_link}')

#Navigate to new_account_link.url to connect account
input = input(f'navigate to {new_account_link.url}, then hit enter')