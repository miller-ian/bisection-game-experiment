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


results = parser2.get_list()

# # process results 
# print("Getting data for experiment: ", 
#       parser2.directory, end="\n\n")
# print("Attributes of a participant: ", 
#       results[0].__dict__.keys(), end="\n\n")

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

# # check outputs
# print("first guesses: ", first_guesses)
# print()
# print("knows bisection search: ", knows_binSearch)
# print()

# # plot the distribution of first guesses
# sns.distplot(first_guesses)

# optimal bisection search 
def bisection_search_global_optimal(secret, lower, upper):
    """
    Returns the optimal bisection search trace if 
    information gain was maximized at every step.
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

# noisy bisection search - Uniform
def bisection_search_uniform(secret, lower, upper):
    """
    Returns a noisy bisection search trace with uniform 
    random guessing over remaining intervals.
    Args:
        secret (int): the secret number to be guessed.
        lower (int): inclusive lower bound of interval.
        upper (int): inclusive upper bound of interval.

    Returns:
        A list of the (noisy) optimal bisection search trace.
    """
    trace = []
    
    # guess by sampling from Unif(a, b)
    a = lower
    b = upper
    guess = int(uniform.rvs(loc=a, scale=b-1))
    
    while guess != secret:
        trace.append(guess)
        # update guess
        if guess < secret: # too low
            lower = guess
        elif guess > secret: # too high
            upper = guess 
        # update guess
        a = lower
        b = upper
        guess = int(uniform.rvs(loc=a, scale=b-a))
        
    # append last guess (which must be the secret number)
    trace.append(guess)
    return trace

# noisy bisection search - Gaussian
def bisection_search_gaussian(secret, lower, upper):
    """
    Returns a noisy bisection search trace with gaussian
    random guessing centered at midpoint and variance 
    inversely proportional to remaining interval size.
    Args:
        secret (int): the secret number to be guessed.
        lower (int): inclusive lower bound of interval.
        upper (int): inclusive upper bound of interval.

    Returns:
        A list of (noisy) optimal bisection search trace.
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

# write a program that sees a partipant's guesses at each turn and outputs
# what they should have guessed at each turn conditioned on previous responses
def bisection_search_conditional(secret, lower, upper, sequence, memLeak=False):
    """
    Returns trace of normative optimal predictions for an agent that 
    maximizes expected information gain at each turn.
    
    Memory Load model: The longer people have been playing,
                    the more likely they are to forget what their current 
                    interval bounds (lower, upper) is. When someone forgets a 
                    bound, they revert to the corresponding default bound of
                    the game (i.e 1 or 10^x)
    
    Args:
        secret (int): the secret number to be guessed.
        lower (int): inclusive lower bound of interval.
        upper (int): inclusive upper bound of interval.
        sequence (list): the guesses of an actual person.
        memLeak (bool): account for memory load in long games
            
    Returns:
        A list of the normative conditional bisection trace.

    """
    UP = upper # global upper bound depends on current game
    trace = [None]*len(sequence)
    
    for t in range(len(sequence)):
        if t > 0:
            # place Memory Load model here if people never 
            # forget their immediately previous guess
            
            # what the person guessed last turn
            pred = sequence[t-1]
            if pred < secret:
                # assumes person remembers lower
                lower = max(lower, pred) 
            elif pred > secret:
                # assumes person remembers upper
                upper = min(upper, pred) 
        
        # place Memory Load model here if people can 
        # forget their immediately previous guess
        if memLeak:
            il = random.random() # pseudo-random float in [0,1]
            iu = random.random() # bounds can 'leak' independently
            # the probablity of a memory leak increases with time
            if il < t/100: # 100 >> max # of guesses 
                lower = 1 # lower bound of all our games is 1
            if iu < t/100:
                upper = UP # upper bound is some power of 10
                
        # midpoint maximizes information
        guess = (upper + lower)//2
        trace[t] = guess
        
    return trace


# get the results of a random single participant
idx = random.randint(0, len(results))
actual_guesses = [int(num) for num in results[idx].responses if num!='null']
secret_num =  actual_guesses[-1]

# get the conditional guesses
informed_guesses = bisection_search_conditional(secret_num, 1, 1000, actual_guesses)
errors = [actual_guesses[i] - informed_guesses[i] for i in 
          range(len(actual_guesses))]
print(errors)