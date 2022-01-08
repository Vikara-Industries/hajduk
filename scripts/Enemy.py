import pygame
import random
from sys import exit
import random
import time
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self,spawn_counter):
        super(Enemy,self).__init__()

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
        self.enemy_aim = pygame.image.load('../sprites/Turk/Aim.png').convert_alpha()

        #Shoot##
        self.shooting = False
        enemy_shoot1 = pygame.image.load('../sprites/Turk/Shoot 1.png').convert_alpha()
        enemy_shoot2 = pygame.image.load('../sprites/Turk/Shoot 2.png').convert_alpha()
        enemy_shoot3 = pygame.image.load('../sprites/Turk/Shoot 3.png').convert_alpha()
        enemy_shoot4 = pygame.image.load('../sprites/Turk/Shoot 4.png').convert_alpha()
        enemy_shoot5 = pygame.image.load('../sprites/Turk/Shoot 5.png').convert_alpha()
        self.enemy_shoot = [enemy_shoot1,enemy_shoot2,enemy_shoot3,enemy_shoot4,enemy_shoot5]

        #Stand###
        self.enemy_stand = pygame.image.load('../sprites/Turk/Stand.png')
#############################################################################
        self.anim_speed = 0.2

        self.image =  pygame.image.load('../sprites/Turk/Stand.png')
        self.image = pygame.transform.scale2x(self.image)

        self.animation_list = pygame.image.load('../sprites/Turk/Stand.png')
        self.animation_index = 0
        self.filp = False


        self.rect = self.image.get_rect()
        self.speed = 3
        self.bilosta = []
        #self.weapon = weapons

        #dettecting collision kurac#OVO IZNAD NE ZANM DA LI RADI
        #self.sight_range = pygame.Rect((self.rect.midleft),(200,400))

        self.spawn_counter = spawn_counter
        self.FOV = math.pi







    def spawn(self):
        position_enemy = []
        POS_X = ('0', '0', ' 700', '700')
        POS_Y = ('380', '164', '380', '164')

        for i in POS_X:
                for a in POS_Y:
                    position_enemy.append([i,a])

                    #ovo gore su kordinate portala, position_enemy sklopi x,y
                    #a u Enemy_position random bira tuple mogucih pozicija gde moze da se stvori
        if self.spawn_counter > 0:
            Enemy_position = random.choice(position_enemy)
            self.rect = self.image.get_rect(midbottom = (int(Enemy_position[0]),int(Enemy_position[1])))
            self.spawn_counter -= 1
        #self.rect = self.image.get_rect(center = (Enemy_position[0],Enemy_position[1]))

            #print(Enemy_position[0], Enemy_position[1])


    def animation(self):
        self.animation_index += self.anim_speed
        #self.image = self.enemy_stand
        if self.walking:
            if self.animation_index >= len(self.enemy_walk):
                self.animation_index =0
            self.image = self.enemy_walk[int(self.animation_index)]

        elif self.shooting:
            self.walking = False
            if self.animation_index >= len(self.enemy_shoot):
                self.animation = 0
            self.image = self.enemy_shoot[int(self.animation_index)]

        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.flip(self.image, self.flip, False)



    def Enemy_movment(self,bilosta):
                walk = random.randint(0,1)
                bilosta.append(walk)
                if bilosta[0] == 1:
                    self.flip = False

                    if self.rect.x+25 > 800:
                        self.rect.x -= 0
                    else:
                        self.rect.x += 2
                    self.walking = True
                    if len(bilosta)/60 > 2:
                        bilosta.clear()
                elif bilosta[0] == 0:

                    if self.rect.x+10 < 0:
                        self.rect.x += 0
                    else:
                        self.rect.x -= 2
                    self.flip = True
                    self.walking = True
                    if len(bilosta)/60 > 2:
                        bilosta.clear()


    def checkCollision(self, level):
        if pygame.sprite.spritecollideany(self, level) != None:

            self.y -= 5

    def sees_player(self):
        self.sight_range
        #self.sight_range.blit(screen)






    def update(self):
        Time = pygame.time.get_ticks()
        start_time = 0
        self.Enemy_movment(self.bilosta)
        self.animation()
    #    self.sees_player()
        self.spawn()
        #print(self.spawn_counter)


        pass
