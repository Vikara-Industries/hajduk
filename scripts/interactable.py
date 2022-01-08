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
    def __init__(self, x, y):
        super(Ammo_box,self).__init__()
        self.animation_list = [pygame.image.load("../sprites/interactables/ammo/position 1.png").convert_alpha()]
        self.animation_list.append(pygame.image.load("../sprites/interactables/ammo/position 2.png").convert_alpha())
        self.animation_list.append(pygame.image.load("../sprites/interactables/ammo/position 3.png").convert_alpha())
        self.animation_list.append(pygame.image.load("../sprites/interactables/ammo/position 4.png").convert_alpha())
        self.animation_list.append(pygame.image.load("../sprites/interactables/ammo/position 5.png").convert_alpha())
        self.animation_list.append(pygame.image.load("../sprites/interactables/ammo/position 6.png").convert_alpha())
        
        self.anim_frame = 0
        self.image = self.animation_list[self.anim_frame]
        self.image = pygame.transform.scale2x(self.image)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.prompt_pos = (self.rect.center[0]-20, self.rect.center[1] - 20)

    def update(self):
        self.anim_frame += 0.2
        if self.anim_frame > len(self.animation_list):
            self.anim_frame = 0
        
        self.image = self.animation_list[int(self.anim_frame)]
        self.image = pygame.transform.scale2x(self.image)

    def draw_prompt(self,screen):
        screen.blit(prompt,self.prompt_pos)
    
    def interact(self, player):
        player.ammo += 5
        self.kill()

class Hp_box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Hp_box,self).__init__()
        self.animation_list = [pygame.image.load("../sprites/interactables/health/position 1.png").convert_alpha()]
        self.animation_list.append(pygame.image.load("../sprites/interactables/health/position 2.png").convert_alpha())
        self.animation_list.append(pygame.image.load("../sprites/interactables/health/position 3.png").convert_alpha())
        self.animation_list.append(pygame.image.load("../sprites/interactables/health/position 4.png").convert_alpha())
        self.animation_list.append(pygame.image.load("../sprites/interactables/health/position 5.png").convert_alpha())
        self.animation_list.append(pygame.image.load("../sprites/interactables/health/position 6.png").convert_alpha())
        
        self.anim_frame = 0
        self.image = self.animation_list[self.anim_frame]
        self.image = pygame.transform.scale2x(self.image)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)
        self.prompt_pos = (self.rect.center[0]-20, self.rect.center[1] - 20)

    def update(self):
        self.anim_frame += 0.2
        if self.anim_frame > len(self.animation_list):
            self.anim_frame = 0
        
        self.image = self.animation_list[int(self.anim_frame)]
        self.image = pygame.transform.scale2x(self.image)

    def draw_prompt(self,screen):
        screen.blit(prompt,self.prompt_pos)
    
    def interact(self, player):
        player.hp += 1
        self.kill()