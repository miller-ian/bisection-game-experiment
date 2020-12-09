#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 00:45:02 2020

@author: quileesimeon
"""

import parser2
import seaborn as sns

# process results 
print("Getting data for experiment: ", parser2.directory)
results = parser2.get_list()
print("Attributes of a participant: ", 
      results[0].__dict__.keys())

# get the data for the first guess
first_guesses = []
# logical vector capturing binary search knowledge
knows_binSearch = [] 
for participant in results:
    responses = participant.responses
    familiar = 1 if participant.binary_search_familiar else 0
    if responses:
        resp = responses[0]
        if resp != 'null':
            first_guesses.append(int(resp))
            knows_binSearch.append(familiar)

# check outputs
print(first_guesses)
print(knows_binSearch)

# # plot the first guess
# sns.distplot(first_guesses)

# optimal bisection search trace
def bisection_search_optimal(secret, lower, upper):
    """
    Args:
        secret (int): the secret number to be guessed.
        lower (int): inclusive lower bound of interval.
        upper (int): inclusive upper bound of interval.

    Returns:
        A list of the optimal bisection search trace.
    """
    trace = []
    guess = (upper + lower)//2
    while guess != secret:
        trace.append(guess)
        # update guess
        if guess < secret: # too low
            lower = guess
        elif guess > secret: # too high
            upper = guess 
        guess = (upper + lower)//2
    # append last guess (which must be the secret number)
    trace.append(guess)
    return trace
    
    