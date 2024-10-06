"""
Asset Credits:
Background by 97kasunifernando:  https://www.freepik.com/premium-photo/quotvibrant-treasure-island-scenequot_274285067.htm#fromView=search&page=2&position=25&uuid=9fac35a5-1d49-4747-aecc-c91e0332b17e 
10K Most Common Words By MIT: https://www.mit.edu/~ecprice/wordlist.10000
Map UI by vectortraditon: https://www.vecteezy.com/vector-art/49315197-8-bit-pixel-art-medieval-paper-scroll-parchment
Pirate by Yael Wiss: https://www.alamy.com/8bit-pixel-art-of-a-pirate-character-holding-a-sword-image544561793.html?imageid=AFE12213-54A1-4EC3-8154-E79C39B1EE28&p=727716&pn=1&searchId=3df74e98ecbad3eeca088bc1ee48ce8c&searchtype=0
"""

import pygame
from sys import exit
from manager import Manager
from settings import *


def intConvertable(str):
    try:
        int(str)
    except ValueError:
        return False
    else:
        return True

def eventLoop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                translator.updateWord("left")
            
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                translator.updateWord("right")
            
            elif event.key == pygame.K_SPACE: 
                translator.updateSentence()
                
                if translator.wordCount >= 10:
                    translator.previousWordCount = 10
                    translator.wordCount = 0
                    if not translator.hasTranslated:
                        translator.hasTranslated = True
                        manager.handleTranslationChanges()
                    translator.translate()
            
            elif event.key == pygame.K_RETURN:
                translator.previousWordCount = translator.wordCount
                translator.wordCount = 0
                if not translator.hasTranslated:
                    translator.hasTranslated = True
                    manager.handleTranslationChanges()
                translator.translate()
            
            elif event.key == pygame.K_RSHIFT:
                if not manager.indexInput == "TYPE NUM":
                    translator.wordIndex = int(manager.indexInput)
                    translator.currentWord = translator.wordList[translator.wordIndex]
                    testList = translator.savedSentence.split(" ")
                    if len(testList) != 1:
                        # This removed the caps from the first word
                        testList[0] = testList[0][0].lower() + testList[0][1:]
                    if translator.currentWord in testList:
                        translator.updateWord("right")
                    manager.indexInput = "TYPE NUM"
            
            else:
                key = pygame.key.name(event.key)
                key = key.replace("[", "").replace("]", "")
                if intConvertable(key):
                    if manager.indexInput == "TYPE NUM":
                        manager.indexInput = key
                    elif len(manager.indexInput) < 4:
                        manager.indexInput = manager.indexInput[0:] + key

def main():
    global manager, translator
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    background = pygame.image.load("graphics/background.PNG").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    manager = Manager()
    translator = manager.translator
    
    pygame.display.set_caption("THY MATEY TRANSLATOR")
    while True:
        eventLoop()
        screen.blit(background, (0, 0))
        manager.draw(screen)
        manager.drawSpecial()
        manager.update()
        clock.tick(FPS)
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    main()