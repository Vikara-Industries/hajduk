import pygame
import random
from sys import exit
import random
import time


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
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


        self.rect = self.image.get_rect(midbottom = (300,300))
        self.speed = 3

        #self.weapon = weapons


    def animation(self):
        self.anim_speed += self.anim_speed
        #self.image = self.enemy_stand
        if self.walking:
            if self.animation_index >= len(self.enemy_walk):
                self.animation =0
            self.image = self.enemy_walk[int(self.animation_index)]

        elif self.shooting:
            self.walking = False
            if self.animation_index >= len(self.enemy_shoot):
                self.animation =0
            self.image = self.enemy_shoot[int(self.animation_index)]

        self.image = pygame.transform.scale2x(self.image)




    def Enemy_movment(self):
            walk = random.randint(0,1)
            if walk == 1:
                self.rect.x += 5
                self.walking = True
            elif walk == 0:
                self.rect.x -= 5
                self.walking = True


    def checkCollision(self, level):
        if pygame.sprite.spritecollideany(self, level) != None:

            self.y -= 5

    def sees_player(self,Player, sight_range):
        pass





    def update(self):
        self.Enemy_movment()
        self.animation()

        pass
