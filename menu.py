import pygame, sys, personnages
from pygame.locals import *
import constantes as const

FramePerSec = pygame.time.Clock()

class MenuGauche(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/Menu_Gauche.png") 
        self.rect = self.image.get_rect()
        self.rect.center = (const.ZONE_MORTE//2, (const.SCREEN_HEIGHT//2))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Arrièreplan(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sprites/temp.png") 
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT//2))
        self.rect.bottom = const.SCREEN_HEIGHT

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self):
        self.rect.move_ip(0,1)
        if (self.rect.bottom > const.SCREEN_HEIGHT+512):
            self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT//2))
            self.rect.bottom = const.SCREEN_HEIGHT
            

def ChoixPerso():
    #Choix perso
    FramePerSec.tick(const.FPS)
    Joueur = personnages.Player(1)
    AP=Arrièreplan()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        V1 = personnages.Player(1)
        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.move()
        AP.draw(personnages.DISPLAYSURF)
        V1.rect.center = ((const.SCREEN_WIDTH//2)-200,const.SCREEN_HEIGHT//2)
        V1.draw(personnages.DISPLAYSURF)
        V2 = personnages.Player(2)
        V2.rect.center = (const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT//2)
        V2.draw(personnages.DISPLAYSURF)
        V3 = personnages.Player(3)
        V3.rect.center = ((const.SCREEN_WIDTH//2)+200,const.SCREEN_HEIGHT//2)
        V3.draw(personnages.DISPLAYSURF)
        Joueur.update()
        Joueur.draw(personnages.DISPLAYSURF)
        if pygame.sprite.collide_rect(Joueur,V1):
            return 1
        elif pygame.sprite.collide_rect(Joueur,V2):
            return 2
        elif pygame.sprite.collide_rect(Joueur,V3):
            return 3
        pygame.display.update()
        FramePerSec.tick(const.FPS)
    
def AfficheScore(valeur):
    font = pygame.font.Font('freesansbold.ttf', 32)
    Score=font.render(str(valeur), True, const.GREEN, const.GRIS)
    scorerect=Score.get_rect()
    scorerect.center=(const.ZONE_MORTE//2,const.SCREEN_HEIGHT-125)
    personnages.DISPLAYSURF.blit(Score,scorerect)

def ChoixMode():
    #Choix du mode de jeu
    FramePerSec.tick(const.FPS)
    Joueur = personnages.Player(1)
    V1 = personnages.Player(1)
    
    V1.rect.center = ((const.SCREEN_WIDTH//2)-150,const.SCREEN_HEIGHT//2)
    
    V2 = personnages.Player(2)
    V2.rect.center = ((const.SCREEN_WIDTH//2)+150,const.SCREEN_HEIGHT//2)
    
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        personnages.DISPLAYSURF.fill(const.WHITE)
        V1.draw(personnages.DISPLAYSURF)
        V2.draw(personnages.DISPLAYSURF)
        Joueur.update()
        Joueur.draw(personnages.DISPLAYSURF)

        if pygame.sprite.collide_rect(Joueur,V1):
            return 1
        elif pygame.sprite.collide_rect(Joueur,V2):
            return 2
       
        pygame.display.update()
        FramePerSec.tick(const.FPS)