import pygame, sys
from pygame.locals import QUIT
from pygame import mixer

import random
import time

pygame.init()

e = False

Screen_Width = 1000
Screen_Height = 800
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Monster_Dudes_Project")

clock = pygame.time.Clock()

FPS = 60


Main_Dude_Front = pygame.image.load("Images/Main_Dude_Front.png")

Birdle_Front = pygame.image.load("Images/Birdle_Front.png")
Birdle_Back = pygame.image.load("Images/Birdle_Back.png")

Main_Dude_Front = pygame.transform.scale(Main_Dude_Front,(55,50))

Birdle_Front = pygame.transform.scale(Birdle_Front,(300,200))
Birdle_Back = pygame.transform.scale(Birdle_Back,(300,200))

Texts = [" has appeared!",["Run","Attack","Catch","Change Monster"],"What do you do","'s HP: "]

#class Moves():
    #def __init__(self,name,damage,type):
        #self.name = name
        #self.damage = damage
        #self.type = type

#poke = Moves("Poke",10,0)
#slap = Moves("Slap",30,0)

class Textbox(pygame.sprite.Sprite):
    def __init__(self,x,y,xsize,ysize):
        super().__init__()
        self.x = x
        self.y = y
        self.xsize = xsize
        self.ysize = ysize
        self.image = pygame.Surface((xsize,ysize), pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        self.image.fill("White")
        self.rect = self.image.get_rect(topleft = (self.x,self.y))

class Text():
    def __init__(self,text,x,y,size,index):
        self.text = text
        self.size = size
        self.index = index

        self.font=pygame.font.Font(None,self.size)

        self.x = x
        self.y = y
        self.display_text = self.font.render(self.text,False,self.color(player))


    def color(self,bro):
        if self.index == bro.text_index:
            return "Yellow"
        else:
            return "Black"
        
        
    def show_text(self):
        screen.blit(self.display_text,(self.x,self.y))

    def action(self):
        pass



class Monsters(pygame.sprite.Sprite):
    def __init__(self,x,y,name,lv,front_image,back_image,stats):
        super().__init__()

        self.x = x
        self.y = y

        self.name = name

        self.lv = lv

        self.front_image = front_image
        self.back_image = back_image

        self.hp_ratio = stats[0]
        self.attack_ratio = stats[1]
        self.defense_ratio = stats[2]

        self.hp = self.hp_ratio * self.lv
        self.maxhp = self.hp
        self.attack = self.attack_ratio * self.lv
        self.defense = self.defense_ratio * self.lv

    def load_monster(self):
        self.x += 5

    def display_monster(self,bro):
        if self in bro.monsters:
            self.x = 100
            self.y = 400
            screen.blit(bro.monsters[bro.current_monster].back_image,(self.x,self.y))
        else:
            screen.blit(self.front_image,(self.x,self.y))

Birdle = Monsters(0,100,"Birdle",5,Birdle_Front,Birdle_Back,[1,1,1,1])
        

    

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.text_index = 0

        self.x = x
        self.y = y

        self.monsters = [Birdle]
        self.current_monster = 0

        self.your_turn = True
        self.spawn_chance = 0

        self.deltax = 0
        self.deltay = 0

        self.can_control = True
        self.battling = False

        self.image = Main_Dude_Front
        self.image.convert_alpha()
        self.rect = self.image.get_rect(center = (self.x,self.y))

    def display_monster(self):
        screen.blit(self.monsters[self.current_monster].back_image,(100,500))


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

    def text_move(self):
        global e
        if key[pygame.K_LEFT] and not e:
            self.text_index -= 1
            e = True
        elif key[pygame.K_RIGHT] and not e:
            self.text_index += 1
            e = True

        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            e = False

        if self.text_index > 3:
            self.text_index = 3
        elif self.text_index < 0:
            self.text_index = 0
        

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
            random_num = random.randint(0,1000)
            if random_num <= dude.spawn_chance:
                dude.spawn_chance = 0
                print("YOO")
                player.can_control = False
                return True
            else:
                dude.spawn_chance +=1
                return False
    
if True:
    player = Player(Screen_Width/2,Screen_Height/2)
    wall = Terrain(100,100,"Brown")
    grass = Grass(100,300,"Green")

    event_text = Textbox(0,650,1000,200)
    player_stats = Textbox(650,400,350,200)
    enemy_stats = Textbox(0,0,350,200)

    game_sprites = pygame.sprite.Group()
    game_sprites.add(wall)
    game_sprites.add(grass)
    game_sprites.add(player)

    textboxs_sprites = pygame.sprite.Group()
    textboxs_sprites.add(event_text)
    textboxs_sprites.add(player_stats)
    textboxs_sprites.add(enemy_stats)

    initiated = False
    radius = 0
    transition_circle = pygame.Surface((radius*2, radius*2),pygame.SRCALPHA, 32)
    transition_circle.fill("Black")

################################################

    keepGameRunning = True

while keepGameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
           keepGameRunning = False

################################################
#code between hashtags is from https://www.geeksforgeeks.org/how-to-set-up-the-game-loop-in-pyggame/
    screen.fill("Gray")   

    if player.can_control:    
        key = pygame.key.get_pressed()


    if not player.battling:
        player.move()
        player.update_position()
        wall.block(player)
        grass.battle_true(player)
        game_sprites.draw(screen)
        screen.blit(transition_circle,((Screen_Width/2)-radius,(Screen_Height/2)-radius))

    if not player.can_control:
        if radius < 1000:
            player.rect.centerx -= player.deltax
            player.rect.centery -= player.deltay
            radius += 5
            transition_circle = pygame.Surface((radius*2, radius*2),pygame.SRCALPHA, 32)
            transition_circle.fill("Black")
        else:
            player.battling = True

    if player.battling:

        # immediately draw textboxes, as they are on the lowest layer below the text and graphics
        textboxs_sprites.draw(screen)

        if not initiated:

            #defines texts and enemys needed for battle

            enemy = Monsters(0,100,"Birdle",random.randint(2,5),Birdle_Front,Birdle_Back,[1,1,1,1])

            appear_text = Text(enemy.name+Texts[0],100,700,100,None)
            enemy_hp_text = Text(str(enemy.hp)+" / "+ str(enemy.maxhp)+" HP",100,80,80,None)
            enemy_name_text = Text(enemy.name,20,20,50,None)
            enemy_lv_text = Text("Lv: " + str(enemy.lv), 180, 20, 50,None)

            attack_text = Text("Attack",100,700,50,0)
            run_text = Text("Run",300,700,50,1)
            catch_text = Text("Catch",450,700,50,2)
            change_text = Text("Change Monster",650,700,50,3)

            actions_list = [attack_text,run_text,catch_text,change_text]


            initiated = True

        if not player.can_control:
            # transition from overworld to battle, enemy moves on screen and text says they have appeared
            enemy.load_monster()
            appear_text.show_text()

            if enemy.x > 650:
                player.can_control = True

        else:
            enemy_name_text.show_text()
            enemy_lv_text.show_text()
            enemy_hp_text.display_text = enemy_hp_text.font.render(enemy_hp_text.text,False,enemy_hp_text.color(player)) ##text.text IK IK
            enemy_hp_text.show_text()

            #BATTLE LOOP
            if player.your_turn:

                player.text_move()
                player.monsters[player.current_monster].display_monster(player)

                for action in actions_list:
                    action.display_text = action.font.render(action.text,False,action.color(player)) ##text.text IK IK
                    action.show_text()



        
        enemy.display_monster(player)

    pygame.display.flip()


    clock.tick(FPS)

pygame.quit()
sys.exit()
