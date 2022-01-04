import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon):
        super(Player,self).__init__()
        self.image = pygame.image.load("player.png").convert_alpha()
        
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = 10
        self.sneaking = False
        self.weapon = weapon
        #noise should be its own class later, this shit is confusing to read
        self.noise_img = pygame.image.load("noise.png")
        self.noise_rect = self.noise_img.get_rect()
        self.noise_rect.center = self.rect.center
    
    def update(self):
        self.input()
        self.y += 5
        self.checkCollision()
        self.rect.center = (self.x, self.y)

        if self.moving and not self.sneaking:
            self.make_noise()


    def input(self):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()

        if keys[pygame.K_a]: 
            self.x -= self.speed
            self.moving = True
        else: self.moving = False

        if keys[pygame.K_d]: 
            self.x += self.speed
            self.moving = True
        else: self.moving = False

        if keys[pygame.K_LCTRL]:
            self.speed = 3
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
            if self.y > 315:
                self.y = 315
        elif self.y > 375:
            self.y = 375
            
    def make_noise(self):
        pass