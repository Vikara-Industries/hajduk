from os import path
import pygame
from pygame import mouse
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon):
        super(Player,self).__init__()

        #animation
        self.flip = False
        self.animation_list = [pygame.image.load("../sprites/turk/Stand.png").convert_alpha()]

        self.idle = [pygame.image.load("../sprites/turk/Stand.png").convert_alpha(),pygame.image.load("../sprites/turk/Stand.png").convert_alpha()]

        self.aiming = False
        self.aim = [pygame.image.load("../sprites/turk/aim.png").convert_alpha(),pygame.image.load("../sprites/turk/aim.png").convert_alpha()]
        
        self.moving = False
        self.walking = []
        self.walking.append(pygame.image.load("../sprites/turk/walk 1.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 2.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 3.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 4.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 5.png").convert_alpha())
        self.walking.append(pygame.image.load("../sprites/turk/walk 6.png").convert_alpha())

        self.shooting = False
        self.shooting_anim = []
        
        self.frame_index = 0
        
        self.image = self.animation_list[self.frame_index]
        self.image = pygame.transform.scale2x(self.image)
        
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = 5

        self.sneaking = False


        self.weapon = weapon
        self.shot = False
        #noise should be its own class later, this shit is confusing to read
        self.noise_img = pygame.image.load("../sprites/noise.png")
        #self.noise_img = pygame.transform.scale2x(self.noise_img)
        self.noise_img = pygame.transform.rotozoom(self.noise_img,0,2)
        self.noise_rect = self.noise_img.get_rect()
    

    #seperate the shit that uses screen into a seperate UI class
    def update(self,level):
        if not self.shooting:
            self.input()
        self.animate()
        self.y += 5
        self.checkCollision(level)
        self.rect.center = (self.x, self.y)

    def animate(self):
        if self.moving:
             self.animation_list = self.walking
             self.weapon.spread_min = 160
        elif self.aiming: 
            self.animation_list = self.aim
            self.weapon.spread_min = 40
        else: self.animation_list = self.idle
        
        self.frame_index += 0.2
        if self.frame_index > len(self.animation_list):
            self.frame_index = 0

        self.image = self.animation_list[int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)
        self.image = pygame.transform.flip(self.image, self.flip, False)


    def draw_ui(self,screen):
        if self.moving and not self.sneaking:
            self.make_noise(screen)
            self.weapon.spread = self.weapon.spread_max

        if self.aiming:
            pygame.draw.line(screen,(255,0,0),self.rect.center, (mouse.get_pos()[0] ,mouse.get_pos()[1] + self.weapon.spread/5))
            pygame.draw.line(screen,(255,0,0),self.rect.center, (mouse.get_pos()[0] ,mouse.get_pos()[1] - self.weapon.spread/5))
        
        if self.shot:
            pygame.draw.circle(screen, (255,100,200), self.shot,3,2)

    def input(self):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()
        if mouse_keys[2] == True:
            self.aiming = True
            self.weapon.aim()
        else: self.aiming = False

        if mouse_keys[0] == True:
            self.shot = self.weapon.shoot(self.rect.center, pygame.mouse.get_pos())
            

        if keys[pygame.K_d]: 
            self.x += self.speed
            self.moving = True
            self.flip = False

        elif keys[pygame.K_a]: 
            self.x -= self.speed
            self.moving = True
            self.flip = True

        else: 
            self.moving = False


        if keys[pygame.K_r]:
            self.weapon.reload()

        if keys[pygame.K_LCTRL]:
            self.speed = 2.5
            self.sneaking = True
        else:
            self.speed = 5
            self.sneaking = False


    def checkCollision(self, level):
        if pygame.sprite.spritecollideany(self, level) != None:
            
            self.y -= 5

    def make_noise(self, screen):
        self.noise_rect.center = (self.x, self.y)
        screen.blit(self.noise_img, self.noise_rect)