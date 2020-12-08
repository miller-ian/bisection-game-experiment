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
for participant in results:
    responses = participant.responses
    if responses:
        resp = responses[0]
        if resp != 'null':
            first_guesses.append(int(resp))

print(first_guesses)

sns.distplot(first_guesses)