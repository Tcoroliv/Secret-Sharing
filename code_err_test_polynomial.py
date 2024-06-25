#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from code_err_function import code_err

import random
import numpy as np
import matplotlib.pyplot as plt











########## DEFINE RANGES OF SEVERAL PARAMETERS ##########

# Create an array with ranges for the field size

field_sizes = [11, 29, 47, 71, 97]

# Create an array with 10 numbers of parties for each field size

def get_nums_prts(field_size):
    nums_prts = []
    nums_prts.append(2)
    aux = (field_size-2)//9
    for i in range(1,9):
        nums_prts.append(2+i*aux)
    nums_prts.append(field_size)
    return nums_prts
    
# Create an array with at most 10 thresholds for each number of parties

def get_thrs(num_prts):
    thrs = []
    if num_prts <= 10:
        thrs = range(1,num_prts+1)
    else:
        thrs.append(1)
        aux = (num_prts-1)//9
        for i in range(1,9):
            thrs.append(1+i*aux)
        thrs.append(num_prts)
    return thrs











########## DEFINES THE SECRET SHARING SCHEME AND SOME ATTACKS ##########

# Define Shamir's secret sharing

def shamir(field_size, num_prts, thr, mes):
    shrs = [poly_eval(mes,i+1,field_size) for i in range(0,num_prts)]
    return shrs

# Define an auxiliary function for shamir

def poly_eval(poly_coefs, eval_pt, field_size):
    res = poly_coefs[0]
    for i in range(1,len(poly_coefs)):
        res += poly_coefs[i] * eval_pt**i
    return res % field_size

# Define the attack (low-degree polynomial)

def poly_aux(num_sums, degree, coefs, prts):

    def poly(x, field_size):
        sum = 0
        for i in range(0,num_sums):
            prod = coefs[i]
            for j in range(0,degree[i]):
                prod *= x[prts[i][j]]
            sum += prod
        return quant_number(sum,field_size)

    return poly

# Define auxiliary function for the attack

def quant_number(x, field_size): #quantization of a number
    if field_size % 2 == 0:
        if x >= field_size // 2:
            x = 1
        else:
            x = 0
    else:
        if x > field_size // 2:
            x = 1
        else:
            if x < field_size // 2:
                x = 0
            else:
                x = random.randint(0,1)                  
    return x











########## ITERATIONS OF THE VARIOUS PARAMETERS ##########

# Create two arrays to create a scatter plot of error versus threshold/number of parties

x = []
y = []

# Iterations for field sizes

for i in range(0,len(field_sizes)):
    
    field_size = field_sizes[i]
    nums_prts = get_nums_prts(field_size)
    
    # Iterations for number of parties
    
    for j in range(0,len(nums_prts)):

        num_prts = nums_prts[j] # Number of parties
        thrs = get_thrs(num_prts)
        
        # Iterations for thresholds
        
        for k in range(0,len(thrs)):

            thr = thrs[k] # Threshold
            max_epsilon = 0
            
            # Iterations for different functions
            
            for l in range(0,30): 
                
                # Randomize the polynomial
                
                num_sums = random.randint(1,9)
                degree = [random.randint(0,9) for m in range(0,num_sums)]
                coefs = [random.randint(0,field_size-1) for n in range(0,num_sums)]
                prts = [[random.randint(0,num_prts-1) for p in range(0,degree[q])] for q in range(0,num_sums)]
                
                
                # Compute the error
                
                epsilon = code_err(field_size, num_prts, thr, poly_aux(num_sums,degree,coefs,prts), shamir, 30) 
                    
                if epsilon > max_epsilon:
                    max_epsilon = epsilon
                    
            x.append(thr/num_prts)
            y.append(max_epsilon)
            
            
            
            
            
            
            
            
            
            
            
########## CREATE A SCATTER PLOT OF ERROR VERSUS THRESHOLD/NUMBER OF PARTIES ##########

plt.scatter(x, y)

# Convert x and y to numpy arrays

x = np.array(x)
y = np.array(y)

# Perform linear regression using numpy polyfit

slope, intercept = np.polyfit(x, y, 1)

# Calculate the predicted y values

y_pred = slope * x + intercept

# Plot the results

plt.scatter(x, y, label='Data Points')
plt.plot(x, y_pred, color='red', label='Linear Fit')
plt.xlabel('Threshold / Number of Parties')
plt.ylabel('Error')
plt.title('Linear Regression of Error vs Threshold/Num Parties')
plt.legend()
plt.show()

# Print the slope and intercept

print(f"Slope: {slope}, Intercept: {intercept}")