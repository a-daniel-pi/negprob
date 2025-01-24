# This file does the actual sampling

import random

# Probability that this is true
LEFT = lambda s00, s01, s10, s11: s10+s11
RIGHT = lambda s00, s01, s10, s11: s01+s11
SAME = lambda s00, s01, s10, s11: s00+s11

def sample(s00, s01, s10, s11, form):
    '''This function atually does the sampling.'''
    total = s00+s01+s10+s11
    if total != 1:
        raise ValueError("Probabilities msut sum to 1")

    return form(s00, s01, s10, s11) > random.random()

def sample3000(s00, s01, s10, s11):
    '''Calculates 1000 samples for each type of sample'''
    lsample = rsample = ssample = 0
    for i in range(1000):
        lsample += sample(s00, s01, s10, s11, LEFT)
        rsample += sample(s00, s01, s10, s11, RIGHT)
        ssample += sample(s00, s01, s10, s11, SAME)

    return lsample, rsample, ssample