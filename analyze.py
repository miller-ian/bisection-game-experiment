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
# set the appropirate upper bound depending on experiment
UPPER = 1000 # 10 for small-, 1000 for mid-, 100000 for big-interval

# # check parser attributes
# print("Getting data for experiment: ", 
#       parser2.directory, end="\n\n")
# print("Attributes of a participant: ", 
#       results[0].__dict__.keys(), end="\n\n")

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
        if memLeak and t>15 and t<25:
            il = random.random() # pseudo-random float in [0,1]
            iu = random.random() # bounds can 'leak' independently
            # the probablity of a memory leak increases with time
            if il < t/500: # 100 >> max # of guesses 
                lower = random.choice(sequence[:t-1])
                # lower = 1 # lower bound of all our games is 1
            if iu < t/500:
                upper = random.choice(sequence[:t-1])
                # upper = UP # upper bound is some power of 10
                
                
        # midpoint maximizes information
        guess = (upper + lower)//2
        trace[t] = guess
        
    return trace


# get the data for the first guesses
first_guesses = []
# binary search prior knowledge logical vector 
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

# get guess sequence data as lists to be analyzed in MATLAB
# a list of the number guesses taken by players until game end
actual_gameLengths = []
# a list of the number of guesses the optimal algorithm would take
optimal_gameLengths = []
# a list of list of deviations from EIG maximizing guesses
delta_sequences = []
# a list of list of deviations from leaky EIG maximizing guesses
delta_leaky_sequences = []
# below are not strictly needed
# a list of all the secret numbers
secret_numbers = []
# a list of people's actual guess sequences
experiment_guessSequences = []
# a list of optimal bisection guesses
optimal_guessSequences = []
# a list of the EIG maximizing guesses - no memory leak
EIGmax_guessSequences = []
# a list of the EIG maximizing guesses - with memory leak
EIGmax_memLeak_guessSequences = []

for idx in range(len(results)):
    # actual guess by participant
    actual_guesses = [int(num) for num in results[idx].responses if num!='null']
    secret_num =  actual_guesses[-1]
    # optimal guesses with pure bisection search
    optimal_guesses = bisection_search_global_optimal(secret_num, 1, UPPER)
    # expected information gain maximizing guesses
    informed_guesses = bisection_search_conditional(secret_num, 1, UPPER, actual_guesses)
    # expected information gain maximizing memory leaky guesses
    informed_leaky_guesses = bisection_search_conditional(secret_num, 1, UPPER, actual_guesses, memLeak=True)
    # calculate the absolute error of the participant
    errors = [min(UPPER, abs(actual_guesses[i] - informed_guesses[i])) for 
              i in range(len(actual_guesses))]
    leaky_errors = [min(UPPER, abs(actual_guesses[i] - informed_leaky_guesses[i])) for 
              i in range(len(actual_guesses))]
    
    # output vectors
    actual_gameLengths.append(len(actual_guesses))
    optimal_gameLengths.append(len(optimal_guesses))
    delta_sequences.append(errors)
    delta_leaky_sequences.append(leaky_errors)
    # extra outputs
    secret_numbers.append(secret_num)
    experiment_guessSequences.append(actual_guesses)
    optimal_guessSequences.append(optimal_guesses)
    EIGmax_guessSequences.append(informed_guesses)
    EIGmax_memLeak_guessSequences.append(informed_leaky_guesses)
    
# # check outputs
# print("real game lengths: ", actual_gameLengths)
# print()
# print("optimal game lengths: ", optimal_gameLengths)
# print()
# print("search deltas: ", delta_sequences)
# print()
    
    
for l in delta_leaky_sequences:
    print(l, ";")
    
    
    
    
    
    
    
    
    
    
    