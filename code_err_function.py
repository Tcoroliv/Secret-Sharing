#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

def code_err(field_size, num_prts, thr, fun, code, num_iters):

    sum_val1 = 0
    sum_val2 = 0

    for i in range(num_iters):

        # Generate a random sequence u with size num_prts

        u = [random.randint(0,field_size-1) for j in range(0,num_prts)]

        # Compute f(u)

        val1 = fun(u,field_size)

        # Generate a message (secret + other (thr-1) random field elements)

        mes = [random.randint(0,field_size-1) for k in range(0,thr)]

        # Compute f(X)

        codeword = code(field_size,num_prts,thr,mes)

        val2 = fun(codeword,field_size)

        # Update sum values

        sum_val1 += val1
        sum_val2 += val2

    # Estimate the expected values of f(U) and f(X)

    exp_val1 = sum_val1 / num_iters
    exp_val2 = sum_val2 / num_iters
    
    # Compute the error

    return abs(exp_val1-exp_val2)