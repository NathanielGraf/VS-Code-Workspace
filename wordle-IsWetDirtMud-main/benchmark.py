#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

from multiprocessing import Pool

from wordle import *
from solver import *

first_word = None

def experiment(idx):
    return GameManager(Solver(first_word)).play_game()

num_trials = 1000
num_guesses = []
with Pool(12) as p:
    for winner in p.imap_unordered(experiment, range(num_trials)):
        num_guesses.append(winner)

print("computing density")
density = gaussian_kde(num_guesses)
print("generating histogram")
plt.hist(num_guesses, bins=(list(set(num_guesses + [0,1,2,3,4,5,6]))), density=True)
plt.xlabel("Number of guesses")
plt.ylabel("Proportion of words solved")
print("generated histogram")
fn = "solver_data.pdf"
plt.savefig(fn)
print("saved to", fn)
print("expected number of guesses:", float(sum(num_guesses)) / float(len(num_guesses)))
