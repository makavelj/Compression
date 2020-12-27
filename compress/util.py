'''
General util functions for compression.
'''

import random
import math
import random
import numpy as np


#Compute integer values for a word
def word_to_int(omega):
    set = []
    for c in omega:
        set.append(ord(c))
    return set

#Creates string based on integers
def int_to_word(A):
    string = ""
    for e in A:
        string += chr(e)
    return string

#Randomized quicksort implementation with list comprehension
def quicksort(A):
    if len(A) <= 1: return A

    pivotindex = random.randint(0, len(A)-1)
    pivot = A[pivotindex]

    equal = [x for x in A if x == pivot]
    lesser = [x for x in A if x < pivot]
    greater = [x for x in A if x > pivot]

    return quicksort(lesser) + equal + quicksort(greater)

#Create list of the alphabet for a word
def word_alphabet(omega):
    dict = {}
    alphabet = []
    j = 0
    for c in omega:
        if(not(c in dict)):
            dict[c] = j
            j += 1
            alphabet.append(c)
    return(alphabet)

#Create dictionary to access index in array
def dictionary(alphabet):
    dict = {}
    i = 0
    for letter in alphabet:
        dict[letter] = i
        i += 1
    return(dict)

#Compute the number of occurences of every letter
def letter_count(omega, sigma=None, alphabet=None):
    n = len(omega)
    #If no alphabet table availabe create one one on the fly
    if(alphabet==None):
        alphabet = word_alphabet(omega)
        alphabet = sorted(alphabet)
    #If no dictionary availabe to access index create one on the fly
    if(sigma==None): sigma = dictionary(alphabet)
    count = [0]*len(alphabet)
    for i in range(n):
        letter = sigma[omega[i]]
        count[letter] +=1
    return count

#Compute all Cyclic shifts
def cyclic_shifts(factors):
    rotations = []
    m = len(factors)
    for i in range(m):
        concat = factors[i] + factors[i]
        n = len(factors[i])
        for j in range(n):
            rotations.append(concat[j:j+n])
    return rotations

#sorting based on comparing infinite periodic repetitions
def ipr_sort(R):
    max = -1
    n = len(R)
    for i in range(n):
        if(len(R[i]) > max):
            max = len(R[i])
    ipr = []
    for i in range(n):
        inf = R[i]
        while(len(inf) < max):
            inf += R[i]
        ipr.append([inf, i])
    sorting_order = quicksort(ipr)
    sorted_order = [""]*n
    for i in range(n):
        sorted_order[i] = R[sorting_order[i][1]]
    return sorted_order

#Computing the prefix array for knuthm morris pratt
def preprocess(P):
    m = len(P)
    pi = [0]*m
    j = 0
    for i in range(1,m):
        if(P[i] == P[j]):
            j += 1
        else:
            j = 0
        pi[i] = j
    return pi

#Computing all matches of a Pattern in String
def knuth_morris_pratt(T, P):
    n = len(T)
    m = len(P)
    prefix = preprocess(P)
    j = 0
    match = []
    for i in range(n):
        while( j > 0 and P[j] != T[i]):
            j = prefix[j-1]
        if(T[i] == P[j]):
            j += 1
        if(j == m):
            match.append(i-m+1)
            j = prefix[j-1]
    return match

#Converts a decimal number into a binary string
def decimal2binary(decimal):
    decimal_str = str(decimal)
    decimal_diggits = [""]*2
    after = False
    for diggit in decimal_str:
        if(diggit == "."): after = True
        if(after == False): decimal_diggits[0] += diggit
        if(diggit != "." and after == True): decimal_diggits[1] += diggit
    bin_val = bin(int(decimal_diggits[0]))
    binary_int = ""
    str(bin_val)
    for i in range(2, len(bin_val)): binary_int += bin_val[i]
    binary_int += "."
    binary_float = ""
    decimal_float = int(decimal_diggits[1])
    for i in range(len(decimal_diggits[1])):
        decimal_float = float(decimal_float/10)
    while(decimal_float != 1.0):
        decimal_float = 2*decimal_float
        if(decimal_float > 1):
            binary_float += '1'
            decimal_float -= 1
        elif(decimal_float < 1):
            binary_float += '0'
    binary_float += '1'
    return(binary_int + binary_float)

#Compute entropy of information
def entropy(X):
    information = 0
    n = len(X)
    word_count = letter_count(X)
    word_prob = [count / n for count in word_count]
    for probability in word_prob:
        information += probability * math.log(1/probability, 2)
    return information

#Split data into training and test set
def split_data(X, y, frac=0.3, max_samples=None, seed=None):
    if seed is not None:
        np.random.seed(seed)
    indices = np.random.permutation(len(X))
    indices = indices[:max_samples]
    indices_test, indices_train = indices[:int(len(indices)*frac)], indices[int(len(indices)*frac):]
    X_train, X_test = X[indices_train], X[indices_test]
    y_train, y_test = y[indices_train], y[indices_test]
    return X_train, X_test, y_train, y_test
