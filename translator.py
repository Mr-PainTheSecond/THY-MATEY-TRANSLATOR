import pygame
from random import randint
from settings import *

class Translator():
    def __init__(self) -> None:
        self.importWordList()
        self.wordIndex = randint(0, len(self.wordList) - 1)
        self.currentWord = self.wordList[self.wordIndex]
        self.savedSentence = "mom "
        self.translatedSentence = ""
        self.hasTranslated = False
        print(self.currentWord)
    
    def translate(self):
        self.translatedSentence = self.savedSentence.split(" ")
        self.savedSentence = ""
        for index, word in enumerate(self.translatedSentence):
            if word.lower() in GREETING_WORDS:
                self.translatedSentence[index] = word.replace(word, "Ahoy!")
            elif word.lower() in NOUN:
                self.translatedSentence[index] = word.replace(word, "Matey")
        
        self.translatedSentence = " ".join(self.translatedSentence) 
            
    
    def updateWord(self, direction):
        if direction == "left":
            self.wordIndex -= 1
            if self.wordIndex < 0:
                self.wordIndex = len(self.wordList) - 1
            
            self.currentWord = self.wordList[self.wordIndex]
        
        elif direction == "right":
            self.wordIndex += 1
            if self.wordIndex >= len(self.wordList):
                self.wordIndex = 0
            
            self.currentWord = self.wordList[self.wordIndex]
    
    def updateSentence(self):
        if self.savedSentence == "":
            # Uppercase the first letter of the word
            upperCase = self.currentWord[0].upper()
            self.savedSentence = upperCase + self.currentWord[1:] + " "
        else:
            self.savedSentence += self.currentWord + " "
        self.wordIndex = randint(0, len(self.wordList) - 1)
        self.currentWord = self.wordList[self.wordIndex]
        print(self.savedSentence)
    
    def importWordList(self):
        # Import the 10K most commonly used words, according to MIT
        textFile = "info/10K_Words.txt"
        with open(textFile, "r") as commonWords:
            words = commonWords.read()
        self.wordList = words.split("\n")
    

        