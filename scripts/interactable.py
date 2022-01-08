import pygame

prompt = pygame.image.load("../sprites/interactables/prompt.png")

class Hide(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Hide,self).__init__()
        self.image = pygame.image.load("../sprites/interactables/Hide.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.prompt_pos = (self.rect.center[0]-20, self.rect.center[1] - 20)

    def update(self):
        pass
    def draw_prompt(self,screen):
        screen.blit(prompt,self.prompt_pos)

    def interact(self, player):
        player.hiding = True

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Portal,self).__init__()
        self.image = pygame.image.load("../sprites/interactables/portal.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.prompt_pos = (self.rect.center[0]-20, self.rect.center[1] - 20)

    def update(self):
        pass
    def draw_prompt(self,screen):
        screen.blit(prompt,self.prompt_pos)

    def interact(self, player):
        if player.y > 150:
            player.y -= 210
        else:
            player.y += 210


class Ammo_box(pygame.sprite.Sprite):
    pass
class Hp_box(pygame.sprite.Sprite):
    pass
