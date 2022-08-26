#!/usr/bin/env python3

from ast import pattern
from copy import deepcopy
from distutils.log import info
from wordle import *
import math

class Solver(Player):
    
    def __init__(self):
       
        #Defines the WordList() class as a variable
        self.wordlist = WordList()
        
        #Sets the number of guesses to 0
        self.num_guesses = 0
        
        #Creates a list of all possible guesses
        self.allwords=[]
        with open('BigProjects/wordle-NathanielGraf-main/words.txt') as fp:
            self.allwords = fp.readlines()
        self.allwords = [x.strip() for x in self.allwords]

    #This function finds the next best guess
    def findNextGuess(self):
        
        #Sets the length of the wordlist to a variable
        length = len(self.wordlist)
        
        #Prints to see runtime kinda
        print(length)
        
        #If 1 goal word possible, guess it
        if length == 1:
            return self.wordlist[0]
        
        #Defines the max entropy starter
        maxentropy = 0
        
        #For every word in the wordlist, pick every other word in the to be the goal word, and see how much information is gained on average
        for tempguess in self.allwords:
            
            #Defines the entropy list
            entropylist = []
            
            #Prints tempguess so I can see the word we are on
            print(tempguess)
            
            #Skips all words that are the same as the tempgoal word
            for tempgoal in self.wordlist:
                if tempguess == tempgoal: 
                    continue
                
                #Makes a copy of our wordlist we can refine without messing up the original
                templist = deepcopy(self.wordlist)
                
                #Refines our templist according to the current guess and goal word, removes not possible words
                templist.refine(Information(tempgoal, tempguess))
               
                #If the length of the templist is less than 2, assign the full entropy of the list to the entropylist
                if len(templist) < 2: 
                    entropylist.append(math.log2(length))
                    
                #If not, calculate the entropy of the templist and append it to the entropylist
                else:
                    entropylist.append((math.log2(length)) - (math.log2(len(templist))))
            
            #The total word entropy is the average of the entropylist
            entropyforword = (sum(entropylist)) / len(entropylist)   
            
            #Prints for sanity
            print(entropyforword)
            
            #If this new average beats the current champ, replace it
            if entropyforword > maxentropy:
                maxentropy = entropyforword 
                bestguess = tempguess
                
        #Print the best word so I can see it
        print("Best guess: ", bestguess)      
        print("Max Entropy: ", maxentropy)      
        
        #Return guess   
        return bestguess
    
    def findNextGuessWinner(self):
        
        #Sets the length of the wordlist to a variable
        length = len(self.wordlist)
        print(length)
        if length == 1:
            return self.wordlist[0]
        #Defines the list of words to be guessed
        #actualwords = self.wordlist
        maxentropy = 0
        
        #For every word in the wordlist, pick every other word in the to be the goal word, and see how much information is gained on average
        for w in self.allwords:
            currentmax = 0
            totalmax = 10000
            entropylist = []
            print(w)
            for r in self.wordlist:
                if w == r: 
                    continue
                #print(w)
                #print(r)
                templist = deepcopy(self.wordlist)
                
                #print(templist)
                templist.refine(Information(r, w))
                
                if len(templist) > currentmax:
                    currentmax = len(templist)
                
            if currentmax < totalmax:
                totalmax = currentmax
                bestguess = w
    
        print("Best guess: ", bestguess)      
        print("Max Size: ", totalmax)         
        return bestguess
 
    def make_guess(self):
        
        #Guesses trace as first word cause it's the best
        if self.num_guesses == 0: 
            currentguess = "trace"
            self.wordlist.remove(currentguess)
            
        #Runs guess function to find the next best guess, and removes it from the wordlist
        #You can do findNextGuessWinner as well to optimize for smallest list size possible, good for not losing
        else:
            currentguess = self.findNextGuessWinner()
            if currentguess in self.wordlist:
                self.wordlist.remove(currentguess)
        
        #Increment, print, and return guess
        self.num_guesses += 1
        print(currentguess)
        return currentguess

    #Refines the wordlist based on the information given
    def update_knowledge(self, info):
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
