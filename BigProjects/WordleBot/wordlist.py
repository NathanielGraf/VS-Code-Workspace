#!/usr/bin/env python3

from random import choice
import os

class WordList():
    """A list of words. Typically the remaining possible solutions"""

    def __init__(self, word_file = 'BigProjects/wordle-NathanielGraf-main/possible_words.txt', given_words = None):
        """construct a list of words by reading from `word_file`

        If `given_words` is None, read words from `word_file`, otherwise
        populate `self.words` with `given_words` If no `word_file` parameter is
        given, read from "possible_words.txt"

        """
        #Word list is not actually a list 
        #It's an object which encapsulates a list and has useful functions we can use
        
        if given_words is None:
            self.words = []
            with open(word_file) as fp:
                self.words = fp.readlines()
            self.words = [w.strip() for w in self.words]
        else:
            self.words = given_words
            
        
            
        

    def get_random_word(self):
        """returns a random word from the set of words"""
        return choice(self.words)

    def __str__(self):
        return str(self.words)

    def __contains__(self, word):
        return word in self.words

    def __iter__(self):
        return self.words.__iter__()

    def __len__(self):
        return len(self.words)
    
    def __getitem__(self,i):
        return self.words[i]
    
    def remove(self, word):
        return self.words.remove(word)
    
    def __sub__(self, words_to_remove):
        return self.words - words_to_remove
    
    #Subscripting is indexing

    def refine(self, information):
        """updates the words to be consistent with the `information`"""
        #Updating the state of wordlist, updating the words within wordlist
        #For every word in wordlist, we add the word to words if information matches
        #Information matching is bascially finding all the words that match something like, 1 G, A in 3rd spot, no Es, and then it puts them all into words.
        
        words = []
        for word in self.words:
            if information.matches(word):
                words.append(word)
        self.words = words

    def matching(self, pattern, guess):
        """returns the set of words that couldve produced `pattern` in response to `guess`"""
        return [word
                for word in self.words
                if pattern.matches(guess, word)]
