import pygame
import random
from sys import exit
import random
import time
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super(Enemy,self).__init__()
        self.flip = False
        self.xrange = (5,800)
#######Animation###################################
        #Walk
        self.walking = False
        self.enemy_walk_index = 0
        enemy_walk1 = pygame.image.load('../sprites/Turk/Walk 1.png').convert_alpha()
        enemy_walk2 = pygame.image.load('../sprites/Turk/Walk 2.png').convert_alpha()
        enemy_walk3 = pygame.image.load('../sprites/Turk/Walk 3.png').convert_alpha()
        enemy_walk4 = pygame.image.load('../sprites/Turk/Walk 4.png').convert_alpha()
        enemy_walk5 = pygame.image.load('../sprites/Turk/Walk 5.png').convert_alpha()
        enemy_walk6 = pygame.image.load('../sprites/Turk/Walk 6.png').convert_alpha()
        self.enemy_walk = [enemy_walk1,
                            enemy_walk2,
                            enemy_walk3,
                            enemy_walk4,
                            enemy_walk5,
                            enemy_walk6]

        #aim##
        self.aim = False
        self.enemy_aim = [pygame.image.load('../sprites/Turk/Aim.png').convert_alpha(), pygame.image.load('../sprites/Turk/Aim.png').convert_alpha()]
        self.aim_timer = 0
        self.aim_thresh = 3

        #Shoot##
        self.shooting_freeze = 0
        self.shooting = False
        enemy_shoot1 = pygame.image.load('../sprites/Turk/Shoot 1.png').convert_alpha()
        enemy_shoot2 = pygame.image.load('../sprites/Turk/Shoot 2.png').convert_alpha()
        enemy_shoot3 = pygame.image.load('../sprites/Turk/Shoot 3.png').convert_alpha()
        enemy_shoot4 = pygame.image.load('../sprites/Turk/Shoot 4.png').convert_alpha()
        enemy_shoot5 = pygame.image.load('../sprites/Turk/Shoot 5.png').convert_alpha()
        self.enemy_shoot = [enemy_shoot1,enemy_shoot2,enemy_shoot3,enemy_shoot4,enemy_shoot5]

        #Stand###
        self.stand = False
        self.enemy_stand = [pygame.image.load('../sprites/Turk/Stand.png'),pygame.image.load('../sprites/Turk/Stand.png')]
#############################################################################
        self.anim_speed = 0.2

        self.image =  pygame.image.load('../sprites/Turk/Stand.png')
        self.image = pygame.transform.scale2x(self.image)

        self.animation_list = pygame.image.load('../sprites/Turk/Stand.png')
        self.animation_index = 0



        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        self.speed = 3
        self.bilosta = []
        #self.weapon = weapons

        #dettecting collision kurac#OVO IZNAD NE ZANM DA LI RADI
        #self.sight_range = pygame.Rect((self.rect.midleft),(200,400))

        #self.spawn_counter = spawn_counter
        self.FOV = math.pi
        if y < 200:
            if x <300:
                self.xrange = (0,270)
            else: self.xrange = (530,800)






    """ def spawn(self):
        position_enemy = []
        POS_X = ('0', '0', ' 700', '700')
        POS_Y = ('390', '185', '390', '185')

        for i in POS_X:
                for a in POS_Y:
                    position_enemy.append([i,a])

                    #ovo gore su kordinate portala, position_enemy sklopi x,y
                    #a u Enemy_position random bira tuple mogucih pozicija gde moze da se stvori
        if self.spawn_counter > 0:
            Enemy_position = random.choice(position_enemy)
            self.rect = self.image.get_rect(midbottom = (int(Enemy_position[0]),int(Enemy_position[1])))
            self.spawn_counter -= 1
            if self.rect.y < 200:
                if self.rect.x < 400:
                    self.xrange = (0,240)
                else:
                    self.xrange = (500,800) """
        #self.rect = self.image.get_rect(center = (Enemy_position[0],Enemy_position[1]))

            #print(Enemy_position[0], Enemy_position[1])


    def animation(self):
        self.animation_index += self.anim_speed
        #self.image = self.enemy_stand

        if self.shooting:
            if self.animation_index >= len(self.enemy_shoot):
                self.animation_index = 0
            self.image = self.enemy_shoot[int(self.animation_index)]

        elif self.aim:
            if self.animation_index >= len(self.enemy_aim):
                self.animation_index = 0
            self.image = self.enemy_aim[int(self.animation_index)]
        elif self.stand:
            if self.animation_index >= len(self.enemy_stand):
                self.animation_index =0
                self.image = self.enemy_walk[int(self.animation_index)]
        elif self.walking:
            if self.animation_index >= len(self.enemy_walk):
                self.animation_index =0
            self.image = self.enemy_walk[int(self.animation_index)]

        print(self.image)
        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.flip(self.image, self.flip, False)



    def Enemy_movment(self,bilosta):
                walk = random.randint(0,1)
                bilosta.append(walk)
                if bilosta[0] == 1:
                    self.flip = False

                    if self.rect.left in range(self.xrange[0],self.xrange[1]):
                        self.walking = True
                        self.rect.x +=2
                    else:
                        self.stand = True
                        self.rect.x = self.xrange[1]

                elif bilosta[0] == 0:
                    self.flip = True
                    if self.rect.x in range(self.xrange[0],self.xrange[1]):
                        self.rect.x -=2
                    else:
                        self.rect.x = self.xrange[0]

                    self.walking = True
                if len(bilosta)/60 > 2:
                    bilosta.clear()


    def sees(self, player, level):
        if player.hiding:
            return False
        else:
            self.aim = True
            for block in level:
                obscured = block.rect.clipline(self.rect.center, player.hitbox.center)
                if obscured: self.aim = False

            line_to_player = self.rect.clipline(self.rect.center, player.hitbox.center)
            if self.flip:
                if line_to_player[1][0] < line_to_player[0][0]: facing = True
                else: facing = False
            else:
                if line_to_player[1][0] > line_to_player[0][0]: facing = True
                else: facing = False

            if facing and self.aim: return True
            else:                   return False







    def update(self, player, level):
        #self.spawn()
        self.animation()
        self.Enemy_movment(self.bilosta)


        if self.sees(player,level):
            if self.aim_timer < self.aim_thresh:
                self.aim = True
                self.aim_timer += 0.2
            else:
                self.shooting = True
                hit = random.randrange(0,9)
                if hit > 5:
                    player.hp -= 1
                self.aim_timer = 0

                self.wait_for_shoot_anim()


        else: self.aim_timer = 0
