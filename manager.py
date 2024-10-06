import pygame
from math import ceil
from random import randint
from translator import Translator
from settings import *

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, groups, image: pygame.Surface, pos: tuple, name):
        # This class adds the image and rect attribute to the pygame sprite class
        super().__init__(groups)
        self.name = name
        self.image = image
        self.pos = pos
        
        manager: Manager = self.groups()[0]
        self.translator: Translator = manager.translator
        self.screen = pygame.display.get_surface()
        self.rect = self.image.get_rect(center = self.pos)
        self.font = pygame.font.Font(None, 48)
        self.smallerFont = pygame.font.Font(None, 30)
        self.smallFont = pygame.font.Font(None, 24)
        if "//" not in self.name:
            self.specialAttr()
    
    def specialAttr(self):
        if self.name == "map_ui":
            self.currentWord = self.translator.currentWord
        elif self.name == "speech":
            self.laterImage = self.image
            self.laterImage = pygame.transform.scale(self.laterImage, (300, 300))
            self.laterImage = pygame.transform.flip(self.laterImage, True, False)
            self.rect = self.laterImage.get_rect(center = self.pos)
            self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
        elif self.name == "map_score":
            self.image = pygame.transform.scale(self.image, (200, 200))
            self.red = randint(0, 255)
            self.green = randint(0, 255)
            self.blue = randint(0, 255)
            self.shift = 5
            self.rect = self.image.get_rect(topleft = self.pos)

    def wrapText(self, translatorStr: str, fontSurf: pygame.Surface, font: pygame.font.Font):
        numOfLines = ceil(fontSurf.get_width() / (self.rect.width - 175))
        wordList = translatorStr.split(" ")
        wordsPerLine = ceil(len(wordList) / numOfLines)
        currentStr = ""
        currentLine = 1
        for word in range(len(wordList)):
            currentStr += wordList[word] + " "
            if (word % wordsPerLine == 0 and word != 0) or (word == len(wordList) - 1):
                fontSurf = font.render(currentStr, False, "black")
                fontRect = fontSurf.get_rect(topleft = (self.rect.left + 30, self.rect.top + (30 * currentLine)))
                self.screen.blit(fontSurf, fontRect)
                currentLine += 1
                currentStr = ""
                
            
    def scoreDisplay(self): 
        fontSurf = self.font.render("WANTED", False, "black")
        fontRect = fontSurf.get_rect(center = (self.rect.centerx, self.rect.top + 40))
        self.screen.blit(fontSurf, fontRect)
        if self.translator.displayedHighScore:
            scoreStr = "Current Score:"
            score = self.translator.currentScore
        else:
            scoreStr = "High Score:"
            score = self.translator.highScore
        highScoreStr = self.smallerFont.render(scoreStr, False, "black")
        scoreStrRect = highScoreStr.get_rect(center = (self.rect.centerx, self.rect.top + 80))
        self.screen.blit(highScoreStr, scoreStrRect)
        if self.translator.highScoreBeaten:
            self.red += self.shift
            self.green += self.shift
            self.blue += self.shift
            if self.red >= 255 or self.blue >= 255 or self.green >= 255:
                if self.red >= 255: self.red = 255
                if self.blue >= 255: self.blue = 255
                if self.green >= 255: self.green = 255
                self.shift = -5
            if self.red <= 0 or self.blue <= 0 or self.green <= 0:
                if self.red <= 0: self.red = 0
                if self.blue <= 0: self.blue = 0
                if self.green <= 0: self.green = 0
                self.shift = 5
            color = (self.red, self.green, self.blue)
        else:
            color = "black"
        highScoreSurf = self.smallerFont.render(f"{score} pts", False, color)
        highScoreRect = highScoreSurf.get_rect(center = (self.rect.centerx, self.rect.top + 120))
        self.translator.displayedHighScore = not self.translator.displayedHighScore
        self.screen.blit(highScoreSurf, highScoreRect)
            
    def update(self):
        # // Indicates the sprite has no special properties
        if "//" in self.name:
            return
        if self.name == "map_ui":
            countSurf = self.font.render(f"WORD {self.translator.wordIndex}", False, "black")
            countRect = countSurf.get_rect(center = (self.rect.centerx, self.rect.centery - 50))
            self.screen.blit(countSurf, countRect)
            self.currentWord = self.translator.currentWord
            fontSurf = self.font.render(self.currentWord, False, "black")
            fontRect = fontSurf.get_rect(center = self.rect.center)
            self.screen.blit(fontSurf, fontRect)
        elif self.name == "speech" and self.translator.hasTranslated:
            self.translatedSentence = self.translator.translatedSentence
            if self.translator.previousWordCount > 5:
                font = self.smallFont
            else:
                font = self.smallerFont
            fontSurf = font.render(self.translatedSentence, False, "black")
            if fontSurf.get_width() >= self.rect.width - 150:
                self.wrapText(self.translatedSentence, fontSurf, font)
            else:
                fontRect = fontSurf.get_rect(topleft = (self.rect.left + 30, self.rect.top + 30))
                self.screen.blit(fontSurf, fontRect)
        elif self.name == "map_score":
            self.scoreDisplay()
            

class Manager(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.screen = pygame.display.get_surface()
        self.importAssets("graphics/sprites")
        self.font = pygame.font.Font(None, 24)
        self.largeFont = pygame.font.Font(None, 48)
        self.indexInput = "TYPE NUM"
        self.translatedWord = None
    
        
    def importAssets(self, filePath):
        # We add all of the sprites in a path, and 
        surfList = []
        for imgFiles in POSITION_DICT:
            theKey = list(imgFiles.keys())[0]
            fullPath = filePath + "/" + theKey + ".png"
            imgSurf = pygame.image.load(fullPath).convert_alpha()
            surfList.append(imgSurf)
                
        for surf, pos in zip(surfList, POSITION_DICT):
            surfName = list(pos.keys())[0]
            GameSprite(self, surf, pos[surfName], surfName)
    
    def uiDraw(self):
        uiSurf = pygame.Surface((WIDTH, 50))
        uiSurf.fill(UI_COLOR)
        uiRect = uiSurf.get_rect(bottomleft = (0, HEIGHT))
        self.screen.blit(uiSurf, uiRect)
        pygame.draw.rect(self.screen, UI_BORDER, uiRect, 3)
        texts = ["[<-] Previous Word", "[->] Next Word", "[Space] Submit Word", "[Enter] Translate", "[R-SHIFT] Skip to Word", "10 words maximum"]
        xCord = 50
        for text in texts:
            fontSurf = self.font.render(text, False, "black")
            fontRect = fontSurf.get_rect(midleft = (xCord, HEIGHT - 25))
            self.screen.blit(fontSurf, fontRect)
            xCord += fontRect.width + 20
        
        uiSkipSurf = pygame.Surface((200, 200))
        uiSkipSurf.fill(UI_COLOR)
        uiSkipRect = uiSkipSurf.get_rect(midleft = (0, HEIGHT - 200))
        self.screen.blit(uiSkipSurf, uiSkipRect)
        pygame.draw.rect(self.screen, UI_BORDER, uiSkipRect, 3)
        secondTexts = ["SKIP TO", "WORD", self.indexInput]
        yCord = HEIGHT - 270
        for secondText in secondTexts:
            fontSurf = self.largeFont.render(secondText, False, "black")
            fontRect = fontSurf.get_rect(center = (uiSkipRect.centerx, yCord))
            self.screen.blit(fontSurf, fontRect)
            yCord += fontSurf.get_height() + 20
        
    
    def handleTranslationChanges(self):
        bubbleSpeech = [bubble for bubble in self.sprites() if bubble.name == "speech"]
        thePirate = [pirate for pirate in self.sprites() if pirate.name == "pirate"]
        thePirate: GameSprite = thePirate[0]
        bubbleSpeech: GameSprite = bubbleSpeech[0]
        bubbleSpeech.image = bubbleSpeech.laterImage
        # We want the speech bubble to be on the top right of the pirate
        bubbleSpeech.rect = bubbleSpeech.image.get_rect(center = (thePirate.rect.right + 80, thePirate.rect.top))
        
        # bubbleSpeech.image = pygame.transform.scale(bubbleSpeech.laterImage, (WIDTH / 2, HEIGHT / 2))
    
    def drawSpecial(self):
        self.uiDraw()
        
        
            
            