import pygame, sys
from pygame.locals import QUIT
from pygame import mixer

import random
import time

radius = 0

pygame.init()

font=pygame.font.Font(None,50)

Screen_Width = 1000
Screen_Height = 800
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption("Monster_Dudes_Project")

clock = pygame.time.Clock()

FPS = 60

#pygame.mixer.music.load("Music/Battle_Transition.wav")
#pygame.mixer.music.load("Music/Battle.wav")


annoying_flag = False

Main_Dude_Front = pygame.image.load("Images/Main_Dude_Front.png")

Birdle_Front = pygame.image.load("Images/Birdle_Front.png")
Birdle_Back = pygame.image.load("Images/Birdle_Back.png")

Angry_Rat_Front = pygame.image.load("Images/Angry_Rat_Front.png")
Angry_Rat_Back = pygame.image.load("Images/Angry_Rat_Back.png")

Monke_Front = pygame.image.load("Images/Monke_Front.png")
Monke_Back = pygame.image.load("Images/Monke_Back.png")

Main_Dude_Front = pygame.transform.scale(Main_Dude_Front,(55,50))

Birdle_Front = pygame.transform.scale(Birdle_Front,(300,200))
Birdle_Back = pygame.transform.scale(Birdle_Back,(300,200))

Angry_Rat_Front = pygame.transform.scale(Angry_Rat_Front,(300,200))
Angry_Rat_Back = pygame.transform.scale(Angry_Rat_Back,(300,200))

Monke_Front = pygame.transform.scale(Monke_Front,(300,200))
Monke_Back = pygame.transform.scale(Monke_Back,(300,200))


Texts = [" has appeared!",["Run","Attack","Catch","Change Monster"]]

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
    def __init__(self,text,x,y,size,index,function):
        self.text = text
        self.size = size
        self.index = index
        self.function = function

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

    def call_function(self,bro,opponent):
        self.function(bro,opponent)





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
            screen.blit(bro.monsters[bro.curr_mon].back_image,(self.x,self.y))
        else:
            screen.blit(self.front_image,(self.x,self.y))

    def display_hp(self,bro):
        if self in bro.monsters:
            self.hp_text = Text("HP: "+str(self.hp) + "/"+str(self.maxhp),680,520,50,5,None)
        else:
            self.hp_text = Text("HP: "+str(self.hp) + "/"+str(self.maxhp),20,150,50,5,None)
        self.hp_text.show_text()

    def display_name_lv(self,bro):
        if self in bro.monsters:
            self.info_text = Text(str(self.name)+"    lv: "+str(self.lv),680,420,50,5,None)
        else:
            self.info_text = Text(str(self.name)+"    lv: "+str(self.lv),20,20,50,5,None)
        self.info_text.show_text()

    def display_all_info(self,bro):
        self.display_hp(bro)
        self.display_name_lv(bro)

    def attack_opponent(self,opponent,bro):
        opponent.hp -= self.attack

    def enemy_attack(self,bro):
        if random.randint(0,1) == 0:
            self.attack_opponent(bro.monsters[bro.curr_mon],bro)
            bro.event_text = Text(" enemy "+str(self.name)+" attacked "+str(bro.monsters[bro.curr_mon].name)+" and did "+str(self.attack)+" damage ",bro.event_text.x,bro.event_text.y,bro.event_text.size,bro.event_text.index,None)
        else:
            bro.event_text = Text(" enemy "+str(self.name)+" is chillin",bro.event_text.x,bro.event_text.y,bro.event_text.size,bro.event_text.index,None)

    def player_attack(self,opponent,bro):
        self.attack_opponent(opponent,bro)
        bro.event_text = Text(str(bro.monsters[bro.curr_mon].name)+" attacked "+str(opponent.name)+" and did " +str(bro.monsters[bro.curr_mon].attack)+" damage!",bro.event_text.x,bro.event_text.y,bro.event_text.size,bro.event_text.index,None)
            




Birdle = Monsters(0,100,"Birdle",5,Birdle_Front,Birdle_Back,[4,2,3])
Angry_rat = Monsters(0,100,"Angry Rat",5,Angry_Rat_Front,Angry_Rat_Back,[3,5,2])
Monke = Monsters(0,100,"Monke",5,Monke_Front,Monke_Back,[4,2,2])
        
base_monsters = [Birdle,Angry_rat,Monke]
    

class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,actions_list):
        super().__init__()
        self.text_index = 0

        self.x = x
        self.y = y

        self.act_list = actions_list

        self.running = False

        self.monsters = [Monke,Angry_rat,Birdle]
        self.curr_mon = 0

        self.caught_enemy = False

        self.your_turn = True
        self.spawn_chance = 0

        self.deltax = 0
        self.deltay = 0

        self.can_control = True
        self.battling = False

        self.event_text = " "

        self.image = Main_Dude_Front
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

    def text_move(self,list):
        if key[pygame.K_LEFT] and not past_key[pygame.K_LEFT]:
            self.text_index -= 1

        elif key[pygame.K_RIGHT] and not past_key[pygame.K_RIGHT]:
            self.text_index += 1

        #if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:

        if self.text_index > len(list)-1:
            self.text_index = len(list)-1
        elif self.text_index < 0:
            self.text_index = 0
        

    def update_position(self):
        self.rect.centerx += self.deltax
        self.rect.centery += self.deltay

    def run(self,opponent,bro):
        if random.randint(0,1) == 0:
            self.event_text = Text("You ran away (like a stupid dum dum coward )",self.event_text.x,self.event_text.y,self.event_text.size,self.event_text.index,None)
            self.running = True
        else:
            self.event_text = Text("You tried to run but failed :(",self.event_text.x,self.event_text.y,self.event_text.size,self.event_text.index,None)

    def catch(self,opponent,bro):
        if random.randint(0,1) == 0:
            self.event_text = Text("You tried to catch "+str(opponent.name)+" and succeeded!",self.event_text.x,self.event_text.y,self.event_text.size,self.event_text.index,None)
            self.caught_enemy = True
            self.running = True
        else:
            self.event_text = Text("You tried to catch "+str(opponent.name)+" and failed :(",self.event_text.x,self.event_text.y,self.event_text.size,self.event_text.index,None)
            self.caught_enemy = False


    def action(self,opponent,bro):
        if key[pygame.K_z] and not past_key[pygame.K_z]:

            self.act_list[self.text_index].call_function(opponent,bro)
            self.your_turn = False

    def move_next_text_box(self):
        if key[pygame.K_z] and not past_key[pygame.K_z]:
            return True
        else:
            return False

    def show_team(self):
        y = 300
        if key[pygame.K_z]:
            screen.blit(player_team.image,(player_team.x,player_team.y))
            for monster in self.monsters:
                text = font.render(str(monster.name)+"      hp: "+str(monster.hp)+"/"+str(monster.maxhp),False,"Black",None)
                screen.blit(text,(Screen_Width/3,y))
                y += 50

    def reset_to_overworld(self):
        global initiated
        global transition_circle
        global radius
        global stupid_music_flag

        self.battling = False
        self.can_control = True
        self.your_turn = True
        self.running = False

        radius = 0
        initiated = False
        transition_circle = pygame.Surface((radius*2, radius*2),pygame.SRCALPHA, 32)
        stupid_music_flag = False
        pygame.mixer.music.load("Music/Overworld.wav")
        pygame.mixer.music.play(-1)


        
class Terrain(pygame.sprite.Sprite):
    def __init__(self,x,y,xsize,ysize,color):
        super().__init__()
        self.x = x
        self.y = y
        self.xsize = xsize
        self.ysize = ysize
        self.image = pygame.Surface((self.xsize,self.ysize), pygame.SRCALPHA, 32)
        self.image.fill(color)
        self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft =(self.x,self.y))

    def display(self):
        screen.blit(self.image,(self.x,self.y))

    def block(self,dude):
        if dude.rect.colliderect(self.rect):
            dude.rect.centerx -= dude.deltax
            dude.rect.centery -= dude.deltay

class Grass(Terrain):
    def __init__(self,x,y,xsize,ysize,color):
        super(Grass,self).__init__(x,y,xsize,ysize,color)

    def battle_true(self,dude):
        if dude.rect.colliderect(self.rect) and dude.deltax !=0 or dude.rect.colliderect(self.rect) and dude.deltay !=0:
            random_num = random.randint(0,1000)
            if random_num <= dude.spawn_chance:
                dude.spawn_chance = 0
                print("YOO")
                dude.can_control = False
                return True
            else:
                dude.spawn_chance +=1
                return False
            

def transition_to_battle(bro):
    global radius
    global transition_circle
    if radius < 990:
            bro.rect.centerx -= bro.deltax
            bro.rect.centery -= bro.deltay
            radius += 5
            transition_circle = pygame.Surface((radius*2, radius*2),pygame.SRCALPHA, 32)
            transition_circle.fill("Black")
    else:
        bro.battling = True
        radius = 0
        transition_circle = pygame.Surface((radius*2, radius*2),pygame.SRCALPHA, 32)

if True:
    player = Player(Screen_Width/2,Screen_Height/2,[])
    player.event_text = Text(" ",100,700,50,5,None)

    attack_text = Text("Attack",100,700,50,0,player.monsters[player.curr_mon].player_attack)
    run_text = Text("Run",300,700,50,1,player.run)
    catch_text = Text("Catch",450,700,50,2,player.catch)
    change_text = Text("Change Monster",650,700,50,3,None)

    actions_list = [attack_text,run_text,catch_text,change_text]

    player.act_list = actions_list




    wall_top = Terrain(0,0,Screen_Width,50,"Brown")
    wall_left = Terrain(0,0,50,Screen_Height,"Brown")
    wall_bottom = Terrain(0,Screen_Height-50,Screen_Width,50,"Brown")
    wall_right = Terrain(Screen_Width-50,0,50,Screen_Height,"Brown")
    grass = Grass(550,350,Screen_Height-400,Screen_Height-400,"Green")

    event_text = Textbox(0,650,1000,200)
    player_stats = Textbox(650,400,350,200)
    enemy_stats = Textbox(0,0,350,200)

    player_team = Textbox(250,150,500,500)

    textboxs_sprites = pygame.sprite.Group()
    textboxs_sprites.add(event_text)
    textboxs_sprites.add(player_stats)
    textboxs_sprites.add(enemy_stats)

    game_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()

    game_sprites.add(grass)
    game_sprites.add(player)

    wall_sprites.add(wall_top)
    wall_sprites.add(wall_left)
    wall_sprites.add(wall_bottom)
    wall_sprites.add(wall_right)

    initiated = False
    radius = 0
    transition_circle = pygame.Surface((radius*2, radius*2),pygame.SRCALPHA, 32)
    transition_circle.fill("Black")


def overworld_loop():
    global radius
    player.move()
    player.update_position()
    for wall in wall_sprites:
        wall.block(player)
    wall_sprites.draw(screen)
    grass.battle_true(player)
    game_sprites.draw(screen)
    player.show_team()
    screen.blit(transition_circle,((Screen_Width/2)-radius,(Screen_Height/2)-radius))

pygame.mixer.music.load("Music/Overworld.wav")
pygame.mixer.music.play(-1)
################################################

stupid_music_flag = False

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
        overworld_loop()

    if not player.can_control:
        transition_to_battle(player)
        if not stupid_music_flag:
            pygame.mixer.music.load("Music/Battle_Transition.wav")
            pygame.mixer.music.play(0)
            stupid_music_flag = True

    if player.battling:
        player.deltax = 0
        player.deltay = 0

        # immediately draw textboxes, as they are on the lowest layer below the text and graphics
        textboxs_sprites.draw(screen)

        if not initiated:

            #defines texts and enemys needed for battle

            #enemy = Monsters(0,100,"Monke",random.randint(2,5),Monke_Front,Monke_Back,[4,2,3])
            ran_num = random.randint(0,2)

            if ran_num == 0: 
                enemy = Monsters(0,100,"Birdle",5,Birdle_Front,Birdle_Back,[4,2,3])
            elif ran_num == 1:
                enemy = Monsters(0,100,"Angry Rat",5,Angry_Rat_Front,Angry_Rat_Back,[3,5,2])
            else:
                enemy = Monsters(0,100,"Monke",5,Monke_Front,Monke_Back,[4,2,2])
        
        

        
            #enemy = base_monsters[0]

            appear_text = Text(enemy.name+Texts[0],100,700,100,None,None)

            #attack_text = Text("Attack",100,700,50,0,None)
            #run_text = Text("Run",300,700,50,1,player.run)
            #catch_text = Text("Catch",450,700,50,2,player.catch)
            #change_text = Text("Change Monster",650,700,50,3,None)

            #event_text_list = [player.event_text]

            actions_list = [attack_text,run_text,catch_text,change_text]

            pygame.mixer.music.load("Music/Battle.wav")
            pygame.mixer.music.play(-1)


            initiated = True
        if not player.can_control:
            # transition from overworld to battle, enemy moves on screen and text says they have appeared
            enemy.load_monster()
            appear_text.show_text()

            if enemy.x > 650:
                player.can_control = True

        else:
            enemy.display_all_info(player)
            player.monsters[player.curr_mon].display_all_info(player)
            player.monsters[player.curr_mon].display_monster(player)




            #BATTLE LOOP
            if player.your_turn:

                player.text_move(actions_list)
                player.action(enemy,player)

                for action in actions_list:
                    action.display_text = action.font.render(action.text,False,action.color(player))
                    action.show_text()

            else:
                player.event_text.show_text()
                if player.move_next_text_box() and not annoying_flag:
                    if player.running:
                        player.reset_to_overworld()
                        if player.caught_enemy:
                            player.monsters.append(enemy)
                        player.caught_enemy = False
                        annoying_flag = False

                    else:
                        enemy.enemy_attack(player)
                        annoying_flag = True
                    

                elif annoying_flag:
                    if player.move_next_text_box():
                        player.your_turn = True
                        annoying_flag = False





        # enemy is displayed no matter the if else condition because he's there for the opening transition
        enemy.display_monster(player)
        player.deltax = 0
        player.deltay = 0

    past_key = key
    #print(str(player.rect.x) +","+str(player.rect.y))
    pygame.display.flip()


    clock.tick(FPS)

pygame.quit()
sys.exit()
