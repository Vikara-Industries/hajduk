import pygame

class Hide(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Hide,self).__init__()
        self.image = pygame.image.load("../sprites/interactables/Hide.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)