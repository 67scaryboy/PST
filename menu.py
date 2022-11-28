import pygame, sys, personnages
from pygame.locals import *
import constantes as const

FramePerSec = pygame.time.Clock()

def MenuHistoire():
    """
    while True:
        personnages.DISPLAYSURF.fill(const.WHITE)
        AP=Affichage("sprites/AP.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)
        AP.draw(personnages.DISPLAYSURF)
        """
    #Choix du scenario
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    FramePerSec.tick(const.FPS)
    Joueur = personnages.Player(0)

    AP=Affichage("sprites/AP.png",const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT//2) #Fond
    #Armée de bouton pour choisir son lvl
    B1=Affichage("sprites_menu/1.png",const.SCREEN_WIDTH//2-325,const.SCREEN_HEIGHT//2+345)
    B2=Affichage("sprites_menu/2.png",const.SCREEN_WIDTH//2-198,const.SCREEN_HEIGHT//2+230)
    B3=Affichage("sprites_menu/3.png",const.SCREEN_WIDTH//2-90,const.SCREEN_HEIGHT//2+330)
    B4=Affichage("sprites_menu/4.png",const.SCREEN_WIDTH//2+65,const.SCREEN_HEIGHT//2+328)
    B5=Affichage("sprites_menu/5.png",const.SCREEN_WIDTH//2+180,const.SCREEN_HEIGHT//2+233)
    B6=Affichage("sprites_menu/6.png",const.SCREEN_WIDTH//2+170,const.SCREEN_HEIGHT//2+75)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        B1.draw(personnages.DISPLAYSURF)
        B2.draw(personnages.DISPLAYSURF)
        B3.draw(personnages.DISPLAYSURF)
        B4.draw(personnages.DISPLAYSURF)
        B5.draw(personnages.DISPLAYSURF)
        B6.draw(personnages.DISPLAYSURF)
        Joueur.souris(personnages.DISPLAYSURF)
        """"
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
        """
       
        pygame.display.update()
        FramePerSec.tick(const.FPS)

def Animation(listeA, classe):  #Animation d'un objet liée a une classe
                                # ListeA: [a1,a2,a3,...,an,status animation en cours(int)]
    classe.image = pygame.image.load(listeA[listeA[len(listeA)-1]])
    classe.mask = pygame.mask.from_surface(classe.image)
    if listeA[len(listeA)-1]<len(listeA)-2:
        listeA[len(listeA)-1]+=1
    else:
        listeA[len(listeA)-1]=0


def draw_health_bar(surf, pos, size, borderC, backC, healthC, progress):
    pygame.draw.rect(surf, backC, (*pos, *size))
    pygame.draw.rect(surf, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+1, pos[1]+1)
    innerSize = ((size[0]-2) * progress, size[1]-2)
    rect = (round(innerPos[0]), round(innerPos[1]), round(innerSize[0]), round(innerSize[1]))
    pygame.draw.rect(surf, healthC, rect)

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
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    return 1
        elif pygame.sprite.collide_rect(Joueur,V2):
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    return 2
        elif pygame.sprite.collide_rect(Joueur,V3):
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    return 3
        pygame.display.update()
        FramePerSec.tick(const.FPS)
    
def AfficheScore(valeur):
    font = pygame.font.Font('freesansbold.ttf', 32)
    Score=font.render(str(valeur), True, const.GREEN)#, const.BLACK)
    scorerect=Score.get_rect()
    scorerect.center=(100,const.SCREEN_HEIGHT-12)
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

class explosion():
    def __init__(self, origine):
        super().__init__()
        self.image = pygame.image.load("sprites_animation/explosion1.png")#à  modifier
        self.rect = self.image.get_rect()
        self.rect.center=origine.rect.center
        self.time = 0 

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def aff_explo(liste_explo):
    for boom in liste_explo:
        boom.draw(personnages.DISPLAYSURF)
        boom.time +=1
        if boom.time >= 10:
            liste_explo.remove(boom)
        
