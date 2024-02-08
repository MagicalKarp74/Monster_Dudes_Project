import pygame, sys
from pygame.locals import QUIT
from pygame import mixer

import random

pygame.init()

Screen_Width = 1000
Screen_Height = 800
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Monster_Dudes_Project")

clock = pygame.time.Clock()

FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,deltax,deltay):
        self.x = x
        self.y = y
        self.deltax = deltax
        self.deltay = deltay
        self.image = pygame.Surface((30,30), pygame.SRCALPHA, 32)
        self.image.fill("Green")
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center = (self.x,self.y))

    def display(self):
        screen.blit(self.image,(self.x,self.y))

    def move(self):
        if key[pygame.K_LEFT]:
            self.deltax = -4
        elif key[pygame.K_RIGHT]:
            self.deltax = 4
        else:
            self.deltax = 0
            
        if key[pygame.K_UP]:
            self.deltay = -4
        elif key[pygame.K_DOWN]:
            self.deltay = 4
        else:
            self.deltay = 0

    def update_position(self):
        self.x += self.deltax
        self.y += self.deltay

player = Player(Screen_Width/2,Screen_Height/2,0,0)

################################################

keepGameRunning = True

while keepGameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
           keepGameRunning = False
################################################
#code between hashtags is from https://www.geeksforgeeks.org/how-to-set-up-the-game-loop-in-pyggame/
           
    key = pygame.key.get_pressed()
    screen.fill("Blue")
    player.display()
    player.move()
    player.update_position()
    pygame.display.flip()


    clock.tick(FPS)

pygame.quit()
sys.exit()
