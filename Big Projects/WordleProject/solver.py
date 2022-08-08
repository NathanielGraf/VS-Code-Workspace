#!/usr/bin/env python3

from wordle import *

class Solver(Player):
    """
    The Solver Class Defines the Wordle Solver.
    Your task is to fill in this class to automatically play the game.
    """

    def __init__(self):
        """Initialize the solver.

        At the very least, your solver should maintain the number of guesses for
        cooperation with the evaluation script

        """
        self.num_guesses = 0

    def make_guess(self):
        """the make_guess function makes a guess.

        Currently, it always guesses "salty". Write code here to improve your solver.
        For compatibility with the benchmarking script please ensure that you
        always increment the number of guesses when you make a guess

        """
        self.num_guesses += 1
        return "soupy"

    def update_knowledge(self, info):
        """update_knowledge updates the solver's knowledge with an `info` object

        Use this method to update your search state.

        """
        pass


def main():
    solver  = Solver()
    manager = GameManager()
    n_guess = g.play_game()
    print("you found the word in", n_guess, "guesses")

if __name__ == "__main__": main()
