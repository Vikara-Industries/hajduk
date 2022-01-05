import random

class Gun():
    def __init__(self):
        self.spread = 800
        self.spread_max = 800
        self.spread_min = 40
        self.loaded = True
        self.reload_time = 3

    def aim(self):
        if self.spread > self.spread_min:
            self.spread -= 5

    def shoot(self,startpoint, endpoint):
        if self.loaded:

            #add raycast collision check
             
            distance = abs(startpoint[0] - endpoint[0])
            shot_spread = random.randrange(-distance*self.spread, distance*self.spread)/1000
            
            self.spread = self.spread_max
            self.loaded = False

            return (endpoint[0]+shot_spread, endpoint[1]+shot_spread)
        else: return False
    def reload(self):
        self.loaded = True