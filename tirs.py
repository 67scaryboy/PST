import pygame, sys
from pygame.locals import *
import random
import constantes as const


class Tirs(pygame.sprite.Sprite):
      def __init__(self, tireur):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(tireur.rect.center)

      def move(self):
        self.rect.move_ip(0,-3)
        if (self.rect.top < 0):
            self.kill()

      def draw(self, surface):
        surface.blit(self.image, self.rect)