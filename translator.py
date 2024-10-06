import pygame
from random import randint
from settings import *

class Translator():
    def __init__(self) -> None:
        self.importWordList()
        self.wordIndex = randint(0, len(self.wordList) - 1)
        self.currentWord = self.wordList[self.wordIndex]
        self.savedSentence = ""
        self.translatedSentence = ""
        self.wordCount = 0
        self.previousWordCount = 0
        self.hasTranslated = False
        self.highScoreBeaten = False
        self.displayedHighScore = False
        self.getHighScore()
        self.currentScore = 0
    
    def translate(self):
        self.translatedSentence = self.savedSentence.split(" ")
        self.savedSentence = ""
        score = 0
        if randint(1, 5) == 1:
            score += 1000
            self.translatedSentence.insert(0, "Har Har!")
        
        for index, word in enumerate(self.translatedSentence):
            if word.lower() in GREETING_WORDS:
                score += 2000
                self.translatedSentence[index] = word.replace(word, "Ahoy!")
            elif word.lower() in NOUN:
                score += 1000
                self.translatedSentence[index] = word.replace(word, "Matey")
            elif word.lower() in THY:
                score += 3000
                self.translatedSentence[index] = word.replace(word, "thy")
            elif word.lower() in TREASURE:
                score += 2000
                self.translatedSentence[index] = word.replace(word, "thy treasure")
            elif word.lower() in FOES:
                score += 2000
                self.translatedSentence[index] = word.replace(word, "THINE FOES")
            elif word.lower() in BOOZE:
                score += 3000
                self.translatedSentence[index] = word.replace(word, "booze")
            elif word.lower() in BOOTY:
                score += 4000
                self.translatedSentence[index] = word.replace(word, "thy booty")
            elif word.lower() in CREATURE:
                score += 4000
                self.translatedSentence[index] = word.replace(word, "sea creature")
            elif word.lower() in SEA:
                score += 3000
                self.translatedSentence[index] = word.replace(word, "thy mighty sea")
            elif word.lower() in SAND:
                score += 3000
                self.translatedSentence[index] = word.replace(word, "haunted sand")
            elif word.lower() in DEATH:
                score += 7000
                self.translatedSentence[index] = word.replace(word, "thrown overboard...")
            elif word.lower() in HONOR:
                score += 4000
                self.translatedSentence[index] = word.replace(word, "honorable pirate")
            elif word.lower() in PIRATEWORDS:
                score += 5000
            elif randint(1, 7) == 1:
                score += 500
                self.translatedSentence[index] = word.replace(word, "Arghhh!")
            elif randint(1, 15) == 1:
                score += 1000
                self.translatedSentence[index] = word.replace(word, "what the devil?!?")
        
        if randint(1, 5) == 1:
            score += 1000
            self.translatedSentence.append("fire in the hole!")
        
        if randint(1, 10) == 1:
            score += 2000
            self.translatedSentence.append("SEND YER TO THY PLANK!!!")
        
        if randint(1, 100) == 1:
            score += 7000
            self.translatedSentence.append("slayyy girly")
            
        self.currentScore = score
        if score >= self.highScore:
            self.updateHighScore(score)
        
        self.translatedSentence = " ".join(self.translatedSentence) 
            
    
    def updateHighScore(self, newScore):
        scorePath = "info/high_score.txt"
        with open(scorePath, "w") as scoreFile:
            scoreFile.write(str(newScore))
        
        self.highScoreBeaten = True
        self.highScore = newScore
    
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
        
        testList = self.savedSentence.split(" ")
        if len(testList) != 1:
            testList[0] = testList[0][0].lower() + testList[0][1:]
        if self.currentWord in testList:
            self.updateWord(direction)
    
    def updateSentence(self):
        if self.savedSentence == "":
            # Uppercase the first letter of the word
            upperCase = self.currentWord[0].upper()
            self.savedSentence = upperCase + self.currentWord[1:] + " "
        else:
            self.savedSentence += self.currentWord + " "
        self.wordIndex = randint(0, len(self.wordList) - 1)
        self.wordCount += 1
        self.currentWord = self.wordList[self.wordIndex]
    
    def importWordList(self):
        # Import the 10K most commonly used words, according to MIT
        textFile = "info/10K_Words.txt"
        with open(textFile, "r") as commonWords:
            words = commonWords.read()
        self.wordList = words.split("\n")
    
    def getHighScore(self):
        highScorePath = "info/high_score.txt"
        with open(highScorePath, "r") as scoreFile:
            highScore = scoreFile.read()
        
        self.highScore = int(highScore)
    

        