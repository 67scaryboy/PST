import pygame, sys, personnages, pickle, os
from pygame.locals import *
import constantes as const

FramePerSec = pygame.time.Clock()

def Shop():
    Bcontinuer=Affichage("sprites/NContinuer.png",const.SCREEN_WIDTH/2+200,const.SCREEN_HEIGHT/2+150)
    AP=Affichage("sprites_menu/APshop.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)
    MB=Affichage("sprites/mb.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT+70)
    CarteAttaque=Affichage("sprites_menu/Carte1.png",const.SCREEN_WIDTH/2-200,170)
    CarteVie=Affichage("sprites_menu/Carte1.png",const.SCREEN_WIDTH/2+200,170)
    CarteCooldown=Affichage("sprites_menu/Carte1.png",const.SCREEN_WIDTH/2-200,470)
    Joueur = personnages.Player(0)
    VaisseauModifie=1
    V1 = personnages.Player(1)
    V1.rect.center = ((const.SCREEN_WIDTH//2)-200,const.SCREEN_HEIGHT-40)

    V2 = personnages.Player(2)
    V2.rect.center = (const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-40)

    V3 = personnages.Player(3)
    V3.rect.center = ((const.SCREEN_WIDTH//2)+200,const.SCREEN_HEIGHT-40)
    with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir si on à débloqué ou pas les vaisseaux
            temp = pickle.load(f)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        font = pygame.font.SysFont("impact", 20)
        Bcontinuer.modif("sprites/NContinuer.png")
        personnages.DISPLAYSURF.fill(const.WHITE)
        AP.draw(personnages.DISPLAYSURF)
        MB.draw(personnages.DISPLAYSURF)
        CarteAttaque.draw(personnages.DISPLAYSURF)
        CarteCooldown.draw(personnages.DISPLAYSURF)
        CarteVie.draw(personnages.DISPLAYSURF)
        #Affichage argent
        texte=font.render("Composants possédé: " + str(temp['Argent']), True, const.WHITE)#
        texterect=texte.get_rect()
        texterect.center=(const.SCREEN_WIDTH/2+200,const.SCREEN_HEIGHT/2)
        personnages.DISPLAYSURF.blit(texte,texterect)
        Bcontinuer.draw(personnages.DISPLAYSURF)
        V1.draw(personnages.DISPLAYSURF)
        if temp['V2'][0]==True:
            V2.draw(personnages.DISPLAYSURF)
        if temp['V3'][0]==True:
            V3.draw(personnages.DISPLAYSURF)
        Joueur.souris(personnages.DISPLAYSURF)
        if pygame.sprite.collide_rect(Joueur,Bcontinuer): #Bouton chargement de la sauvegarde
            Bcontinuer.modif("sprites/HContinuer.png")
            Bcontinuer.draw(personnages.DISPLAYSURF)
            Joueur.souris(personnages.DISPLAYSURF)
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    return 0
        if pygame.sprite.collide_rect(Joueur,V1):
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    VaisseauModifie = 1
        elif pygame.sprite.collide_rect(Joueur,V2) and temp['V2'][0]==True:
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    VaisseauModifie = 2
        elif pygame.sprite.collide_rect(Joueur,V3) and temp['V3'][0]==True:
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    VaisseauModifie = 3



        pygame.display.update()
        FramePerSec.tick(const.FPS)


def MenuFinPartieArcade(score): # Uniquement à appeler dans la boucle arcade, car affiche les TOPS scores :)
    AP=Affichage("sprites_menu/fond_mort.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            AP=Affichage("sprites_menu/fond_mort.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)
            personnages.DISPLAYSURF.fill(const.WHITE)
            AP.draw(personnages.DISPLAYSURF)
            font = pygame.font.SysFont("impact", 25)
            texte=font.render("Score:", True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2-300,const.SCREEN_HEIGHT/2-30)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render(str(score), True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2-300,const.SCREEN_HEIGHT/2)
            personnages.DISPLAYSURF.blit(texte,texterect)
            with open('topscorearcade.pkl', 'rb') as f:
                temp = pickle.load(f)
            texte=font.render("Meilleurs scores:", True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2+300,const.SCREEN_HEIGHT/2-30)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render(str(temp[1]), True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2+300,const.SCREEN_HEIGHT/2)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render(str(temp[2]), True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2+300,const.SCREEN_HEIGHT/2+30)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render(str(temp[3]), True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2+300,const.SCREEN_HEIGHT/2+60)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render(str(temp[4]), True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2+300,const.SCREEN_HEIGHT/2+90)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render(str(temp[5]), True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2+300,const.SCREEN_HEIGHT/2+120)
            personnages.DISPLAYSURF.blit(texte,texterect)
        if pygame.mouse.get_pressed() == (1, 0, 0): #Clic gauche pour quitter
            break
        pygame.display.update()
        FramePerSec.tick(const.FPS)

def MenuFinPartie(score,victoire): # Paramètre victoire True ou False / Définit quel écran afficher
    AP=Affichage("sprites_menu/fond_mort.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)
    ### Ajoute le score comme argent dans la sauvegarde    
    with open('sauvegarde.pkl', 'rb') as f: #Ouvre le fichier sauvegarde en lecture
        sauvegarde = pickle.load(f) #Le copie dans une variable temporaire
    sauvegarde['Argent']+=score #Ajoute à la variable temporaire le score comme argent
    with open('sauvegarde.pkl', 'wb') as f: #Ouvre le fichier sauvegarde en écriture
        pickle.dump(sauvegarde, f) #Pousse la sauvegarde
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if victoire == False:
            AP=Affichage("sprites_menu/fond_mort.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)
            personnages.DISPLAYSURF.fill(const.WHITE)
            AP.draw(personnages.DISPLAYSURF)
            font = pygame.font.SysFont("impact", 25)
            texte=font.render("Score:", True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2-300,const.SCREEN_HEIGHT/2-30)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render(str(score), True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2-300,const.SCREEN_HEIGHT/2)
            personnages.DISPLAYSURF.blit(texte,texterect)

        else:
            AP=Affichage("sprites_menu/fond_victoire.png",const.SCREEN_WIDTH/2,const.SCREEN_HEIGHT/2)
            personnages.DISPLAYSURF.fill(const.WHITE)
            AP.draw(personnages.DISPLAYSURF)
            font = pygame.font.SysFont("impact", 25)
            texte=font.render("Score:", True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2-300,const.SCREEN_HEIGHT/2-30)
            personnages.DISPLAYSURF.blit(texte,texterect)
            texte=font.render(str(score), True, const.WHITE)
            texterect=texte.get_rect()
            texterect.center=(const.SCREEN_WIDTH/2-300,const.SCREEN_HEIGHT/2)
            personnages.DISPLAYSURF.blit(texte,texterect)

        if pygame.mouse.get_pressed() == (1, 0, 0): #Clic gauche pour quitter
            break
        pygame.display.update()
        FramePerSec.tick(const.FPS)


def MenuHistoire(niveau):
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
    if niveau>0:
        B1=Affichage("sprites_menu/1v.png",const.SCREEN_WIDTH//2-325,const.SCREEN_HEIGHT//2+345)
    else:
        B1=Affichage("sprites_menu/1.png",const.SCREEN_WIDTH//2-325,const.SCREEN_HEIGHT//2+345)
    if niveau>2:
        B2=Affichage("sprites_menu/2v.png",const.SCREEN_WIDTH//2-198,const.SCREEN_HEIGHT//2+230)
    else:
        B2=Affichage("sprites_menu/2.png",const.SCREEN_WIDTH//2-198,const.SCREEN_HEIGHT//2+230)
    if niveau>3:
        B3=Affichage("sprites_menu/3v.png",const.SCREEN_WIDTH//2-90,const.SCREEN_HEIGHT//2+330)
    else:
        B3=Affichage("sprites_menu/3.png",const.SCREEN_WIDTH//2-90,const.SCREEN_HEIGHT//2+330)
    if niveau>4:
        B4=Affichage("sprites_menu/4v.png",const.SCREEN_WIDTH//2+65,const.SCREEN_HEIGHT//2+328)
    else:
        B4=Affichage("sprites_menu/4.png",const.SCREEN_WIDTH//2+65,const.SCREEN_HEIGHT//2+328)
    if niveau>5:
        B5=Affichage("sprites_menu/5v.png",const.SCREEN_WIDTH//2+180,const.SCREEN_HEIGHT//2+233)
    else:
        B5=Affichage("sprites_menu/5.png",const.SCREEN_WIDTH//2+180,const.SCREEN_HEIGHT//2+233)
    if niveau>7:
        B7=Affichage("sprites_menu/7v.png",const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT//2+30)
    else:
        B7=Affichage("sprites_menu/7.png",const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT//2+30)
    if niveau>6:
        B6=Affichage("sprites_menu/6v.png",const.SCREEN_WIDTH//2+170,const.SCREEN_HEIGHT//2+75)
    else:
        B6=Affichage("sprites_menu/6.png",const.SCREEN_WIDTH//2+170,const.SCREEN_HEIGHT//2+75)
    if niveau>8:
        B8=Affichage("sprites_menu/8v.png",const.SCREEN_WIDTH//2-165,const.SCREEN_HEIGHT//2+30)
    else:
        B8=Affichage("sprites_menu/8.png",const.SCREEN_WIDTH//2-165,const.SCREEN_HEIGHT//2+30)
    if niveau>9:
        B9=Affichage("sprites_menu/9v.png",const.SCREEN_WIDTH//2-150,const.SCREEN_HEIGHT//2-125)
    else:
        B9=Affichage("sprites_menu/9.png",const.SCREEN_WIDTH//2-150,const.SCREEN_HEIGHT//2-125)
    if niveau>10:
        B10=Affichage("sprites_menu/10v.png",const.SCREEN_WIDTH//2-15,const.SCREEN_HEIGHT//2-240)
    else:
        B10=Affichage("sprites_menu/10.png",const.SCREEN_WIDTH//2-15,const.SCREEN_HEIGHT//2-240)
    
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
        B7.draw(personnages.DISPLAYSURF)
        B8.draw(personnages.DISPLAYSURF)    
        B9.draw(personnages.DISPLAYSURF)  
        B10.draw(personnages.DISPLAYSURF)
        if niveau>1:
            Atelier=Affichage("sprites/Atelier.png",const.SCREEN_WIDTH//2+200,const.SCREEN_HEIGHT//2-100)
            Atelier.draw(personnages.DISPLAYSURF)
            if pygame.sprite.collide_rect(Joueur,Atelier):
                Atelier.modif("sprites/Atelier_b.png")
                Atelier.draw(personnages.DISPLAYSURF)
                for i in pygame.mouse.get_pressed():
                    if pygame.mouse.get_pressed()[i]==True:
                        Shop() #Ouvre le menu de modifications
        listebouton=[B1,B2,B3,B4,B5,B6,B7,B8,B9,B10]
        Joueur.souris(personnages.DISPLAYSURF)
        for c in range (0,10,1):
            if pygame.sprite.collide_rect(Joueur,listebouton[c]):
                for i in pygame.mouse.get_pressed():
                    if pygame.mouse.get_pressed()[i]==True and c<niveau:
                        return c+1
                    
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
    
    def mouvement(self,x,y):
        self.rect.move_ip(x,y)

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

    with open('sauvegarde.pkl', 'rb') as f: #Chargement de la sauvegarde pour voir si on à débloqué ou pas les vaisseaux
            temp = pickle.load(f)

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
        if temp['V2'][0]==True:
            V2.draw(personnages.DISPLAYSURF)
        if temp['V3'][0]==True:
            V3.draw(personnages.DISPLAYSURF)
        Joueur.souris(personnages.DISPLAYSURF)
        if pygame.sprite.collide_rect(Joueur,V1):
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    return 1
        elif pygame.sprite.collide_rect(Joueur,V2) and temp['V2'][0]==True:
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    return 2
        elif pygame.sprite.collide_rect(Joueur,V3) and temp['V3'][0]==True:
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

def ChoixSauvegarde():
    #Choisir si on charge la sauvegarde ou si on recommence
    pygame.mouse.set_pos(const.SCREEN_WIDTH//2,const.SCREEN_HEIGHT-200)
    FramePerSec.tick(const.FPS)
    Joueur = personnages.Player(0)

    Bcontinuer=Affichage("sprites/NContinuer.png",const.SCREEN_WIDTH//2-150,const.SCREEN_HEIGHT//2) #Bouton arcade
    Brecommencer=Affichage("sprites/NHistoire.png",const.SCREEN_WIDTH//2+150,const.SCREEN_HEIGHT//2) #Bouton historie
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        personnages.DISPLAYSURF.fill(const.WHITE)
        Bcontinuer.modif("sprites/NContinuer.png")
        Bcontinuer.draw(personnages.DISPLAYSURF)
        Brecommencer.modif("sprites/NRecommencer.png")
        Brecommencer.draw(personnages.DISPLAYSURF)
        font = pygame.font.SysFont("arial", 25)
        texte=font.render("Que souhaitez vous faire de votre progression ?", True, const.BLACK)
        texterect=texte.get_rect()
        texterect.center=(const.SCREEN_WIDTH/2,30)
        personnages.DISPLAYSURF.blit(texte,texterect)
        Joueur.souris(personnages.DISPLAYSURF)
        if pygame.sprite.collide_rect(Joueur,Bcontinuer): #Bouton chargement de la sauvegarde
            Bcontinuer.modif("sprites/HContinuer.png")
            Bcontinuer.draw(personnages.DISPLAYSURF)
            Joueur.souris(personnages.DISPLAYSURF)
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    if os.path.exists('sauvegarde.pkl'): #Verifie qu'un fichier sauvegarde existe
                        # Do something if the file exists
                        return 
                    else:
                        # Do something if the file does not exist
                        sauvegarde = {'V1': personnages.V1, #[Vie,Attaque,Cooldown]
                        'V2': personnages.V2,
                        'V3': personnages.V3,
                        'Argent': 0,
                        'Histoire':1} #Attention, cela indique le niveau max auquel le joueur peut jouer. Si 0 tout cassé
                        with open('sauvegarde.pkl', 'wb') as f:
                            pickle.dump(sauvegarde, f)  
                        return  
        elif pygame.sprite.collide_rect(Joueur,Brecommencer): #Bouton recommencer ( :< )
            Brecommencer.modif("sprites/HRecommencer.png")
            Brecommencer.draw(personnages.DISPLAYSURF)
            Joueur.souris(personnages.DISPLAYSURF)
            for i in pygame.mouse.get_pressed():
                if pygame.mouse.get_pressed()[i]==True:
                    sauvegarde = {'V1': personnages.V1, #[Vie,Attaque,Cooldown]
                    'V2': personnages.V2,
                    'V3': personnages.V3,
                    'Argent': 0,
                    'Histoire':1} #Attention, cela indique le niveau max auquel le joueur peut jouer. Si 0 tout cassé
                    with open('sauvegarde.pkl', 'wb') as f:
                        pickle.dump(sauvegarde, f)  
                    return 
       
        pygame.display.update()
        FramePerSec.tick(const.FPS)


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
        
