import scipy.optimize
import numpy as np
from typing import Optional
import math

# we want to minimise | 36 - 4.20 * x1 + 0.69 * x2|
# in standard form this is
# min | c'.x |
#
# where x1 = 1, c = [ 36 4.20 0.69 ]
#
# which is the same as
# min max{ c'.x, -c'.x } s.t. Ax <= b
#
# have to formulate this as 
# min z
#
# such that z >= c'.x
#           z >= -c'.x
# 
# and x has to be integers!

def use_scipy(target: float, max_transactions: Optional[int]):
    # Need to add those slack variables!
    #c = [1]
    #
    #c = [36, -4.2, -0.69]
    #A = 
    pass

def use_cvxpy(target: float, max_transactions: Optional[int]):
    # cvxpy is super cool and does this for us:
    import cvxpy as cp
    x = cp.Variable(2, integer=True)
    MAX_TRANSACTIONS = 50
    constraints = [x >= 0]
    if max_transactions is not None:
        constraints.append(x[0] + x[1] <= MAX_TRANSACTIONS)
    obj = cp.Minimize(cp.abs(4.2*x[0] + 0.69*x[1] - target))
    prob = cp.Problem(obj, constraints)
    prob.solve()
    #print(prob.value)  # error value
    return x.value


def roll_your_own(target: float):
    c_0 = 4.2
    c_1 = 0.69

    payments_by_error = []

    max_c_0 = math.ceil(target / c_0)
    # Should pick c_0 so that it is the max(c_0, c_1)
    for i in range(max_c_0):
        residual = target - c_0 * i
        j = math.floor(residual / c_1)
        payments_by_error.append((residual - j * c_1, i, j))
        j = math.ceil(residual / c_1)
        payments_by_error.append((residual - j * c_1, i, j))

    # Remove negative errors, so that we never underpay
    payments_by_error.sort(key=lambda entry: entry[0])
    filtered = list(filter(lambda entry: entry[0] > 0, payments_by_error))

    # Find the smallest absolute error
    #payments_by_error.sort(key=lambda entry: abs(entry[0]))
    #filtered = payments_by_error

    return (filtered[0][1], filtered[0][2])


a, b = use_cvxpy(36, None)
print(a, b)

a, b = roll_your_own(36)
print(a, b)
