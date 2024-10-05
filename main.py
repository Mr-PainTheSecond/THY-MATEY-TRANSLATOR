"""
Asset Credits:
Background by 97kasunifernando:  https://www.freepik.com/premium-photo/quotvibrant-treasure-island-scenequot_274285067.htm#fromView=search&page=2&position=25&uuid=9fac35a5-1d49-4747-aecc-c91e0332b17e 
10K Most Common Words By MIT: https://www.mit.edu/~ecprice/wordlist.10000
Map UI by vectortraditon: https://www.vecteezy.com/vector-art/49315197-8-bit-pixel-art-medieval-paper-scroll-parchment
"""

import pygame
from sys import exit
from translator import Translator
from manager import Manager
from settings import *

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
            
            elif event.key == pygame.K_RETURN:
                if not translator.hasTranslated:
                    translator.hasTranslated = True
                    manager.handleTranslationChanges()
                translator.translate()

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