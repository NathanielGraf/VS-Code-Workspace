#!/usr/bin/env python3

from ast import pattern
from distutils.log import info
from wordle import *
import math

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
        #i = 0
        
        #self.allposguesses = WordList.words
        self.wordlist = WordList()
        print(len(self.wordlist))
        self.num_guesses = 0

    def findNextGuess(self):
        length = len(self.wordlist)
        actualwords = self.wordlist
    
        for w in self.wordlist:
            maxentropy = 0
            entropylist = []
            
            for r in self.wordlist:
                if w == r: 
                    continue
                print(w)
                print(r)
                templist = actualwords
                
                print(templist)
                templist.refine(Information(r, w))
                print(templist)
                #if len(templist) == 1:
                if len(templist) < 2: 
                    entropylist.append(math.log2(length))
                else:
                    entropylist.append((math.log2(length)) - (math.log2(len(templist))))
                print(entropylist)
            
            entropyforword = (sum(entropylist)) / len(entropylist)   
            
            print(entropyforword)
            if entropyforword > maxentropy:
                maxentropy = entropyforword 
                bestguess = w
                print(bestguess)
                
        print(bestguess)        
        return bestguess
        
 
    def make_guess(self):
        """the make_guess function makes a guess.

        Currently, it always guesses "salty". Write code here to improve your solver.

        For compatibility with the benchmarking script please ensure that you
        always increment the number of guesses when you make a guess

        """
        #A class is a type of thing, and an object is an instance of that thing
        #w = WordList()
        #currentguess = w.get_random_word()
        
        #currentguess = self.allposguesses[i]
        #Player.update_knowledge(Player, currentguess)
        #self.allposguesses.remove(currentguess)
        #i = i + 1
        
        #w.refine(WordList, )
        
                    
        
        #tempWordList.refine(Information(possible_answer, test_guess)
    
        '''
        You have a current word you have guessed:
        currentguess
       
        You want to pick a word from the remaining possible guesses:
        for w in self.wordlist:
         
        Then loop through all possible goal words to see how much this guess with that word will refine the list
        for r in self.wordlist
        
        Take the average of the information gained for each word, and pick the largest one, then guess that word
        entropyforword = []
        entropyforword.append(math.log2(currentlength) - math.log2(len(refinedlist)))
        wordinfo = (sum(entropyforword)) / len(entropyforword)
        
        '''
            
        
        #informationgained = math.log2(currentlength) - math.log2(len(newlength))
       
        if self.num_guesses == 0: 
            currentguess = "irate"
        #elif self.num_guesses == 1:
            #currentguess = "soupy"
        else:
            #currentguess = self.wordlist.get_random_word()
            currentguess = self.findNextGuess()
        self.num_guesses += 1
        self.wordlist.remove(currentguess)
        print(currentguess)
        return currentguess

    def update_knowledge(self, info):
        """update_knowledge updates the solver's knowledge with an `info` object

        Use this method to update your search state.

        """
        self.wordlist.refine(info)
        
    


     
class AllLetterSolver(Player):
    def __init__(self): pass
    def make_guess(self): pass
    def update_knowledge(self, info): pass
    

def main():
    solver  = Solver()
    manager = GameManager(solver)
    n_guess = manager.play_game()
    print("you found the word in", n_guess, "guesses")

if __name__ == "__main__": main()
