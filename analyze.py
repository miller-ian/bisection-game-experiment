#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 00:45:02 2020

@author: quileesimeon
"""

import parser2
import seaborn as sns
import random
from scipy.stats import uniform, norm

# process results 
print("Getting data for experiment: ", 
      parser2.directory, end="\n\n")
results = parser2.get_list()
print("Attributes of a participant: ", 
      results[0].__dict__.keys(), end="\n\n")

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
print("first guesses: ", first_guesses)
print()
print("knows bisection search: ", knows_binSearch)
print()

# # plot the distribution of first guess
# sns.distplot(first_guesses)

# optimal bisection search 
def bisection_search_optimal(secret, lower, upper):
    """
    Returns the optimal bisection seach trace if no feedback
    was given after each decision.
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

# noisy bisection search - uniform
def bisection_search_uniform(secret, lower, upper):
    """
    Returns a noisy bisection seach trace that guesses
    uniform randomly over the reduced interval.
    Args:
        secret (int): the secret number to be guessed.
        lower (int): inclusive lower bound of interval.
        upper (int): inclusive upper bound of interval.

    Returns:
        A list of the optimal bisection search trace.
    """
    trace = []
    # guess by sampling from Unif(lower, upper)
    guess = int(uniform.rvs(loc=lower, scale=upper-1))
    while guess != secret:
        trace.append(guess)
        # update guess
        if guess < secret: # too low
            lower = guess
        elif guess > secret: # too high
            upper = guess 
        # update guess
        guess = int(uniform.rvs(loc=lower, scale=upper-lower))
    # append last guess (which must be the secret number)
    trace.append(guess)
    return trace

# noisy bisection search - normal
def bisection_search_gaussian(secret, lower, upper):
    """
    Returns a noisy bisection seach trace that guesses
    randomly from Gaussian centered at the midpoint of 
    the reduced interval.
    Args:
        secret (int): the secret number to be guessed.
        lower (int): inclusive lower bound of interval.
        upper (int): inclusive upper bound of interval.

    Returns:
        A list of the optimal bisection search trace.
    """
    trace = []
    # guess by sampling from Normal(mu, sigma=1/sqrt(n))
    mu = (upper+lower)//2
    n = (upper-lower+1)
    sigma = 1/(n**0.5)
    guess = int(norm.rvs(loc=mu, scale=sigma))
    while guess != secret:
        trace.append(guess)
        # update guess
        if guess < secret: # too low
            lower = guess
        elif guess > secret: # too high
            upper = guess 
        # update guess
        mu = (upper+lower)//2
        n = (upper-lower+1)
        sigma = 1/(n**0.5)
        guess = int(norm.rvs(loc=mu, scale=sigma))
    # append last guess (which must be the secret number)
    trace.append(guess)
    return trace

# get the results of a random single participant
idx = random.randint(0,len(results))
person_guesses = [int(num) for num in results[idx].responses if num!='null']
secret_num =  person_guesses[-1]
optimal_guesses = bisection_search_optimal(secret_num, 1, 1000)
uniform_guesses = bisection_search_uniform(secret_num, 1, 1000)
normal_guesses = bisection_search_gaussian(secret_num, 1, 1000)

# compare a person's sequence to the globally optimal sequence
print("participant's sequence: ", person_guesses, end="\n\n")
print("optimal sequence: ", optimal_guesses, end="\n\n")

# write a program that sees a person's outputs what the should
# have guess conditioned on previous responses
def bisection_search_conditioned(secret, lower, upper, sequence):
    """
    Returns the running optimal bisection search trace if person
    maximized information gain after each turn.
    
    Args:
        secret (int): the secret number to be guessed.
        lower (int): inclusive lower bound of interval.
        upper (int): inclusive upper bound of interval.
        sequence (list): the guesses of an actual person.
            
    Returns:
        A list of the normative conditioned busection trace.

    """
    trace = [None]*len(sequence)
    
    for count in range(len(sequence)):
        if count > 0:
            # what the person guessed last turn
            pred = sequence[count-1]
            if pred < secret:
                lower = pred
            elif pred > secret:
                upper = pred
        # midpoint maximizes information as first guess
        guess = (upper + lower)//2
        trace[count] = guess
        
    return trace

