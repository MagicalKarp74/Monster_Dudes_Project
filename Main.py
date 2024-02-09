import pygame, sys
from pygame.locals import QUIT
from pygame import mixer

import random
import time

pygame.init()

Screen_Width = 1000
Screen_Height = 800
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Monster_Dudes_Project")

clock = pygame.time.Clock()

FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.spawn_chance = 0
        self.deltax = 0
        self.deltay = 0
        self.can_control = True
        self.battling = False
        self.image = pygame.Surface((30,30), pygame.SRCALPHA, 32)
        self.image.fill("Blue")
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center = (self.x,self.y))

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
        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay

class Terrain(pygame.sprite.Sprite):
    def __init__(self,x,y,color):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((800,80), pygame.SRCALPHA, 32)
        self.image.fill(color)
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center =(self.x,self.y))

    def display(self):
        screen.blit(self.image,(self.x,self.y))

    def block(self,dude):
        if dude.rect.colliderect(self.rect):
            dude.rect.centerx -= dude.deltax
            dude.rect.centery -= dude.deltay

class Grass(Terrain):
    def __init__(self,x,y,color):
        super(Grass,self).__init__(x,y,color)

    def battle_true(self,dude):
        if dude.rect.colliderect(self.rect) and dude.deltax !=0 or dude.rect.colliderect(self.rect) and dude.deltay !=0:
            random_num = random.randint(0,100000)
            if random_num <= dude.spawn_chance:
                dude.spawn_chance = 0
                print("YOO")
                player.can_control = False
                player.battling = True
                return True
            else:
                dude.spawn_chance +=1
                return False



    

player = Player(Screen_Width/2,Screen_Height/2)
wall = Terrain(100,100,"Brown")
grass = Grass(100,300,"Green")

game_sprites = pygame.sprite.Group()
game_sprites.add(wall)
game_sprites.add(grass)
game_sprites.add(player)

################################################

keepGameRunning = True

while keepGameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
           keepGameRunning = False
################################################
#code between hashtags is from https://www.geeksforgeeks.org/how-to-set-up-the-game-loop-in-pyggame/
    if player.can_control:    
        key = pygame.key.get_pressed()
    screen.fill("Gray")


    if not player.battling:
        player.move()
        player.update_position()
        wall.block(player)
        grass.battle_true(player)
        game_sprites.draw(screen)

    

    pygame.display.flip()


    clock.tick(FPS)

pygame.quit()
sys.exit()
