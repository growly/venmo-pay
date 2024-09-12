#!/usr/bin/env python3
# Please excuse gratuitous biz-ing in this file.

import sys
import random

import cvxpy as cp

import venmo_api
from emoji import emojize

# Use the the get_access_token call with your password to get an access token.
#access_token = venmo_api.Client.get_access_token(username='himself@aryaparsi.com', password='')
#print(access_token)
#sys.exit(1)
access_token = 'put your access token here'

client = venmo_api.Client(access_token=access_token)
#users = client.user.search_for_users(query='@calskiclub', username=True)
#for user in users:
#    print(user.username)
#user = client.user.get_user_by_username('@aryareaisparsi')
#print(user)

profile = client.user.get_my_profile()
print(profile)

# get cal ski club id from transactions already made to them
#transactions = client.user.get_user_transactions(user_id=profile.id)
#for transaction in transactions:
#    print(transaction) 

# Greatest ski club of all time
calskiclub_id = '3354877237395456471'

payment_methods_by_id = {}
payment_methods = client.payment.get_payment_methods()
for method in payment_methods:
    payment_methods_by_id[method.id] = method

payment_id = '2322111683100672382'
payment_method = payment_methods_by_id[payment_id]
assert(isinstance(payment_method, venmo_api.models.payment_method.BankAccount))

print(f'using payment method: {payment_method}')

# emoji test
sunglasses = u'\U0001F60E'
pleading_face = u'\U0001F97A'
loveheart = emojize(':red_heart:')
#sunglasses2 = emojize(':smiling_face_with_sunglasses:')
#with open('/tmp/test.txt', 'w') as f:
#    f.write(f'hello {sunglasses}')
#    f.write(sunglasses2)

message = ''''''
words = message.split()
print(len(words))

# We can use cvxpy to find the mix of $4.20 and $0.69 payments that results in
# us paying the closest sum to the dues, $36 (this is a mixed integer program).
# We can optionally constrain it to only a certain number of payments at most
# or (not shown) only allow positive error.
x = cp.Variable(2, integer=True)
MAX_TRANSACTIONS = 50
constraints = [x >= 0,
               x[0] + x[1] <= MAX_TRANSACTIONS]   # Max transactions = 50
obj = cp.Minimize(cp.abs(4.2*x[0] + 0.69*x[1] - 36))
prob = cp.Problem(obj, constraints)
prob.solve()
#print(x.value)
#print(prob.value)

payments = [4.20] * int(x[0]) + [0.69] * int(x[1])
random.shuffle(payments)

payments = payments + [0.69]

print(sum(payments))

#num_payments = len(payments)
#for i in range(0, num_payments):
#    word = 'cssc forever'
#    payment = payments[i]
#    note = f'{loveheart}  {word} {loveheart}  [{i + 1}/{num_payments}]'
#    print(f'payment {i}: {payment} {note}')
#    client.payment.send_money(amount=payment,
#                              note=note,
#                              target_user_id=calskiclub_id,
#                              funding_source_id=payment_id)

client.log_out(f'Bearer {access_token}')
