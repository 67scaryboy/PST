import pygame, sys
from pygame.locals import *
import random, menu, pickle, fight
import constantes as const


DISPLAYSURF = pygame.display.set_mode((const.SCREEN_WIDTH,const.SCREEN_HEIGHT))
DISPLAYSURF.fill(const.WHITE)
pygame.display.set_caption("Game")

###Stats de bases des vaisseaux joueurs###
V1 = [True,100,0,70,0,10,0] # [Débloqué ?, Vie, Nb amélioration vie, Attaque, Nb amélioration attaque, Cooldown, Nb amélioration cooldown]
V2 = [False,130,0,70,0,20,0] 
V3 = [False,150,0,150,0,30,0]


class Enemy(pygame.sprite.Sprite):
      def __init__(self, id):
        super().__init__()
        self.active = 1

        ##### Enemis spéciaux (boss, enemis uniques... A ne pas faire apparaitre traditionellement dans les combats) -> ID négatif
        if id == -1: #Boss niveau 7
            self.image = pygame.image.load("sprites_boss/boss2.png").convert_alpha()
            self.PV = 20000 #PV de ce type d'adversaire
            self.MAXPV = self.PV
            self.ATK = 30 #Attaque de ce type d'adversaire
            self.score = 1000 #Score crédité en cas de kill (a voir, le crédit de score se fera peut etre manuellement)
            self.id = 'b2' #ID de ce type
        elif id == -2:
            self.image = pygame.image.load("sprites_boss/sbires.png").convert_alpha()
            self.PV = 160
            self.MAXPV = self.PV
            self.ATK = 15
            self.score = 30
            self.id = 's1' #Sbire 1

        ##### Enemis traditionnels -> ID positif
        elif id == 1:#Tir sinusoidaux
            self.image = pygame.image.load("sprites/e1.png").convert_alpha()
            self.PV = 100 #PV de ce type d'adversaire
            self.MAXPV = self.PV
            self.ATK = 10 #Attaque de ce type d'adversaire
            self.score = 10 #Score crédité en cas de kill
            self.id = 'e1' #ID de ce type
        elif id == 2:#Tir triple
            self.image = pygame.image.load("sprites/e2.png").convert_alpha()
            self.PV = 150
            self.MAXPV = self.PV
            self.ATK = 30
            self.score = 50
            self.id = 'e2'
        elif id == 3:#Tir standard
            self.image = pygame.image.load("sprites/e3.png").convert_alpha()
            self.PV = 200
            self.MAXPV = self.PV
            self.ATK = 50
            self.score = 100
            self.id = 'e3'
        elif id == 4: #Kamikaze
            self.image = pygame.image.load("sprites/e4.png").convert_alpha()
            self.PV = 100
            self.MAXPV = self.PV
            self.ATK = 70
            self.score = 70
            self.id = 'e4'
        elif id == 5: #Tir diagonaux
            self.image = pygame.image.load("sprites/e5.png").convert_alpha()
            self.PV = 1000
            self.MAXPV = self.PV
            self.ATK = 30
            self.score = 100
            self.id = 'e5'
        elif id == 6: #Tanks
            self.image = pygame.image.load("sprites/e6.png").convert_alpha()
            self.PV = 2000
            self.MAXPV = self.PV
            self.ATK = 70
            self.score = 200
            self.id = 'e6'
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(50,const.SCREEN_WIDTH-50),0)
        self.width = self.image.get_width()
        self.mask = pygame.mask.from_surface(self.image)
      

      #Methodes de déplacement

      def move(self):

        if self.id=='e4':
            pass
        else:
            self.rect.move_ip(0,2)
        if (self.rect.top > const.SCREEN_HEIGHT):
            self.kill()
    
      def moveKamikaze(self, joueur):
        if self.id =='e4':
            if joueur.rect.centery-self.rect.centery<400:
                if joueur.rect.centerx < self.rect.centerx + 10 and joueur.rect.centerx > self.rect.centerx-10:
                    self.rect.move_ip(0,9)
                elif self.rect.centerx < joueur.rect.centerx:
                    self.rect.move_ip(8,6)
                elif self.rect.centerx > joueur.rect.centerx:
                    self.rect.move_ip(-8,6)
            else:
                self.rect.move_ip(0,9)
            if (self.rect.top > const.SCREEN_HEIGHT):
                self.kill()
      
      def moveVitesse(self,VitesseX, VitesseY):
        if self.id=='e4':
            pass
        else:
            self.rect.move_ip(VitesseX,VitesseY)
        if (self.rect.bottom > const.SCREEN_HEIGHT):
            self.kill()


      def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_health(DISPLAYSURF)

      def draw_health(self, surf):
        if self.PV != self.MAXPV:
            health_rect = pygame.Rect(0, 0, self.width, 7)
            health_rect.midbottom = self.rect.centerx, self.rect.bottom
            menu.draw_health_bar(surf, health_rect.bottomleft, health_rect.size, (0, 0, 0), (255, 0, 0), (0, 255, 0), self.PV/self.MAXPV)


class Player(pygame.sprite.Sprite): #Si on
    def __init__(self, id):
        super().__init__()
        if id == 0:#selecteur de perso
            self.image = pygame.image.load("sprites/souris.png").convert_alpha()
            self.id = 'N/A'
            self.PV = 10
            self.MAXPV=self.PV
            self.ATK = 0
            self.cooldown = 100
            self.Ulti = 0
            self.MAXUlti = 1
        if id == 1:
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f) # [Débloqué ?, Vie, Nb amélioration vie, Attaque, Nb amélioration attaque, Cooldown, Nb amélioration cooldown]
            self.image = pygame.image.load("sprites/p1.png").convert_alpha()
            self.id = 'p1'
            self.PV = temp['V1'][1] #a modifier en fonction de perso
            self.MAXPV=self.PV
            self.ATK = temp['V1'][3]
            self.cooldown = temp['V1'][5]
            self.Ulti = 0
            self.MAXUlti = 100
        elif id == 2:
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f) # [Débloqué ?, Vie, Nb amélioration vie, Attaque, Nb amélioration attaque, Cooldown, Nb amélioration cooldown]
            self.image = pygame.image.load("sprites/p2.png").convert_alpha()
            self.id = 'p2'
            self.PV = temp['V2'][1] #a modifier en fonction de perso
            self.MAXPV=self.PV
            self.ATK = temp['V2'][3]
            self.cooldown = temp['V2'][5]
            self.Ulti = 0
            self.MAXUlti = 100
        elif id == 3:
            with open('sauvegarde.pkl', 'rb') as f:
                temp = pickle.load(f) # [Débloqué ?, Vie, Nb amélioration vie, Attaque, Nb amélioration attaque, Cooldown, Nb amélioration cooldown]
            self.image = pygame.image.load("sprites/p3.png").convert_alpha()
            self.id = 'p3'
            self.PV = temp['V3'][1] #a modifier en fonction de perso
            self.MAXPV=self.PV
            self.ATK = temp['V3'][3]
            self.cooldown = temp['V3'][5]
            self.Ulti = 0
            self.MAXUlti = 100
        self.DureeUlti = -1
        self.rect = self.image.get_rect()
        self.rect.center = (const.SCREEN_WIDTH//2, (const.SCREEN_HEIGHT - 50))
        self.mask = pygame.mask.from_surface(self.image)
    
    def draw_health(self, surf):
        health_rect = pygame.Rect(0, 0, self.image.get_width(), 7)
        health_rect.midbottom = self.rect.centerx, self.rect.bottom
        menu.draw_health_bar(surf, health_rect.bottomleft, health_rect.size, 
                (0, 0, 0), (255, 0, 0), (0, 255, 0), self.PV/self.MAXPV)

    def draw_ulti(self, surf):
        health_rect = pygame.Rect(0, 0, self.image.get_width(), 7)
        health_rect.midbottom = self.rect.centerx, self.rect.bottom + 10
        menu.draw_health_bar(surf, health_rect.bottomleft, health_rect.size, 
                (0, 0, 0), (75, 75, 75), (0, 255, 255), 1-self.Ulti/self.MAXUlti)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -7)

        if (self.rect.bottom < const.SCREEN_HEIGHT):
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,7)

        if self.rect.left > const.ZONE_MORTE:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-7, 0)
        if self.rect.right < const.SCREEN_WIDTH:
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(7, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def souris(self,surface):
        self.rect.center = pygame.mouse.get_pos()
        self.draw(surface)

    def ulti(self,enemies,tirs,explo):
        if self.Ulti == self.MAXUlti: 
            if pygame.mouse.get_pressed()[0]:
                if self.id == 'p1': #IEM
                    liste = []
                    for i in range(0,len(enemies)):
                        if enemies[i].id in ['e1','e2','e3']:
                            liste.append(i)
                            explo.append(menu.explosion(enemies[i]))
                    while liste:
                        del enemies[liste.pop()]
                        
                    self.Ulti = 0
                elif self.id == 'p2': #Spam
                    self.DureeUlti = 120
                    self.cooldown = 30
                    self.Ulti = 0
                elif self.id == 'p3': #Laser
                    self.DureeUlti = 300
                    tirs.append(fight.Projectile(self,10,"sprites_animation/laser1.png"))
                    self.cooldown = 300 # pour éviter qu'il tire pendant l'ulti
                    self.Ulti = 0
                else:
                    pass
        else:
            self.Ulti += 1

class Compagon(pygame.sprite.Sprite):
    def __init__(self,perso):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("sprites/compagnon.png"),(20,20)) #pygame.image.load("sprites/compagnon.png") 
        self.ATK = perso.ATK/10
        self.rect = self.image.get_rect()
        self.rect.center = perso.rect.center
        self.rect.right = perso.rect.left-10
        self.deplacementX =0
        self.deplacementY =0
        self.id = 'c1'
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,perso):
        
        #self.rect.center= (perso.rect.right+self.deplacementX,perso.rect.top+ self.deplacementY)
        #if (random.randint(0,1)==1): #Léger déplacement aléatoire du compagnon, a modif pr eviter l'épilepsie
        self.deplacementX+=random.randint(-1,1)
        if ((self.rect.right+self.deplacementX-perso.rect.right<20 or perso.rect.right-self.rect.right<20) and self.rect.right<const.SCREEN_WIDTH and self.rect.left >0):
            self.rect.right = self.rect.right+self.deplacementX
        #else:
        self.deplacementY+= random.randint(-1,1)
        if ((self.rect.top+self.deplacementY-perso.rect.top<10 or perso.rect.top-self.rect.top<10) and self.rect.bottom<const.SCREEN_HEIGHT and self.rect.bottom >0):
            self.rect.bottom = self.rect.top+self.deplacementY
        self.rect.center= (perso.rect.right+self.deplacementX,perso.rect.top+ self.deplacementY)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Debrit(pygame.sprite.Sprite):
    def __init__(self,id,angle):
        super().__init()
        if id == 1:
            self.image =  pygame.image.load("sprites/débrit.png").convert_alpha()
        else:
            self.image =  pygame.image.load("sprites/débrit2.png").convert_alpha()
        self.direction = [0,2]
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
    def move(self):
        self.rect.move_ip(self.direction[0],self.direction[1])
        if (self.rect.top > const.SCREEN_HEIGHT):
            self.kill()
    
    def move(self,traj): #définit une trajectoire et avance
        
        if traj == 0:#base
            self.direction = [0,2]
        if traj == 1:#diagonale \
            self.direction = [1,2]
        elif traj == 2:#diagonale /
            self.direction = [-1,2]
        elif traj == 3:# ->
            self.direction = [2,0]
        elif traj == 4:# <-
            self.direction = [-2,0]

        self.rect.move_ip(self.direction[0],self.direction[1])

    
    def move(self,x,y):
        self.rect.move_ip(x,y)
        if (self.rect.top > const.SCREEN_HEIGHT):
            self.kill()

def crash(debrits, joueur, p_alive):#fonction de colision avec les débrits
    for ferraille in debrits:
        if pygame.sprite.collide_rect(ferraille,joueur): #ajout pour voir si limite les lags
            if pygame.sprite.collide_mask(ferraille,joueur): #colision tirs joueur
                joueur.PV = 0
                p_alive = fight.Mort([],p_P1,debrits)
    return p_alive

def poser_debrits(debrits, id_debrit, posX, posY, angle):
    ferraille  = Debrit(id_debrit, angle)
    ferraille.rect.center=(posX,posY)
    debrits.append(ferraille)