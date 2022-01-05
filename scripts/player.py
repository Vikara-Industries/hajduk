import pygame
from pygame import mouse
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon):
        super(Player,self).__init__()
        self.image = pygame.image.load("../sprites/player.png").convert_alpha()
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
        self.noise_img = pygame.transform.scale2x(self.noise_img)
        self.noise_rect = self.noise_img.get_rect()
    

    #seperate the shit that uses screen into a seperate UI class
    def update(self):
        self.input()
        self.y += 5
        self.checkCollision()
        self.rect.center = (self.x, self.y)


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
            
        #else: self.shot = False

        if keys[pygame.K_a]: 
            self.x -= self.speed
            self.moving = True
        else: self.moving = False

        if keys[pygame.K_r]:
            self.weapon.reload()
        if keys[pygame.K_d]: 
            self.x += self.speed
            self.moving = True
        

        if keys[pygame.K_LCTRL]:
            self.speed = 2.5
            self.sneaking = True
        else:
            self.speed = 5
            self.sneaking = False

    def checkCollision(self):
        if self.x < 0:
           self.x = 0 
        elif self.x > 800 :
            self.x = 800
        
        if self.x > 135 and self.x < 215:
            if self.y > 290:
                self.y = 290
        elif self.y > 350:
            self.y = 350
            
    def make_noise(self, screen):
        self.noise_rect.center = (self.x, self.y)
        screen.blit(self.noise_img, self.noise_rect)
