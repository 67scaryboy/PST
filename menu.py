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

class Affichage(pygame.sprite.Sprite): #Permet l'affichage d'un simple sprite
    def __init__(self, chemin, posX, posY): #chemin=chemin d'accès a l'image a draw
        super().__init__()
        self.image = pygame.image.load(chemin)
        self.rect = self.image.get_rect()
        self.rect.center = (posX, posY)

    def draw(self, surface): #Permet l'affichage
        surface.blit(self.image, self.rect)
    
    def deplacement(self,posX,posY): #Permet de changer sa position
        self.rect.center = (posX, posY)
    
    def modif(self,chemin): #Permet de modifier sa texture
        self.image = pygame.image.load(chemin)

class Arrièreplan(pygame.sprite.Sprite): 
    def __init__(self,n):
        super().__init__()
        if (n==1):
            self.image = pygame.image.load("sprites_paralax/Blue.png").convert_alpha()
        elif (n==2):
            self.image = pygame.image.load("sprites_paralax/red.png").convert_alpha()
        elif (n==3):
            self.image = pygame.image.load("sprites_paralax/Aqua.png").convert_alpha()
        elif (n==4):
            self.image = pygame.image.load("sprites_paralax/big1.png").convert_alpha()
        elif (n==5):
            self.image = pygame.image.load("sprites_paralax/big2.png").convert_alpha()
        elif (n==6):
            self.image = pygame.image.load("sprites_paralax/small1.png").convert_alpha()
        elif (n==7):
            self.image = pygame.image.load("sprites_paralax/small2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT//2))
        self.rect.bottom = const.SCREEN_HEIGHT

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self,v):
        self.rect.move_ip(0,v)
        if (self.rect.bottom > const.SCREEN_HEIGHT+800):
            self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT))
            self.rect.bottom = const.SCREEN_HEIGHT
            

def ChoixPerso():
    #Choix perso
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    FramePerSec.tick(const.FPS)
    Joueur = personnages.Player(0)

    V1 = personnages.Player(1)
    V1.rect.center = ((const.SCREEN_WIDTH//2)-200,const.SCREEN_HEIGHT//2)

    V2 = personnages.Player(2)
    V2.rect.center = (const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT//2)

    V3 = personnages.Player(3)
    V3.rect.center = ((const.SCREEN_WIDTH//2)+200,const.SCREEN_HEIGHT//2)

    AP=Arrièreplan(1)
    AP2=Arrièreplan(5)# 4 ou 5 pour le paralax profond
    AP3=Arrièreplan(6)# 6 ou 7 pour le paralax superieur
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
       
        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.move(1)
        AP2.move(2)
        AP3.move(3)
        AP.draw(personnages.DISPLAYSURF)
        AP2.draw(personnages.DISPLAYSURF)
        AP3.draw(personnages.DISPLAYSURF)
        V1.draw(personnages.DISPLAYSURF)
        V2.draw(personnages.DISPLAYSURF)
        V3.draw(personnages.DISPLAYSURF)
        Joueur.souris(personnages.DISPLAYSURF)
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
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    FramePerSec.tick(const.FPS)
    Joueur = personnages.Player(0)

    Barcade=Affichage("sprites/NArcade.png",const.SCREEN_WIDTH//2-150,const.SCREEN_HEIGHT//2) #Bouton arcade
    Bhistoire=Affichage("sprites/NHistoire.png",const.SCREEN_WIDTH//2+150,const.SCREEN_HEIGHT//2) #Bouton historie
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        personnages.DISPLAYSURF.fill(const.WHITE)
        Barcade.modif("sprites/NArcade.png")
        Barcade.draw(personnages.DISPLAYSURF)
        Bhistoire.modif("sprites/NHistoire.png")
        Bhistoire.draw(personnages.DISPLAYSURF)
        Joueur.souris(personnages.DISPLAYSURF)
        if pygame.sprite.collide_rect(Joueur,Barcade):
            Barcade.modif("sprites/HArcade.png")
            Barcade.draw(personnages.DISPLAYSURF)
            Joueur.souris(personnages.DISPLAYSURF)
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    return 1
        elif pygame.sprite.collide_rect(Joueur,Bhistoire):
            Bhistoire.modif("sprites/HHistoire.png")
            Bhistoire.draw(personnages.DISPLAYSURF)
            Joueur.souris(personnages.DISPLAYSURF)
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    return 2
       
        pygame.display.update()
        FramePerSec.tick(const.FPS)