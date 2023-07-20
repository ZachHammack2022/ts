from ts.envs.utils.ships.ship import Ship
import math
import pygame

class SupplyShip(Ship):
    
   
    def __init__(self, color,image=None,rangee=None,cost=None,refueling_speed=None, max_speed=None, max_health=None, x=None, y=None, speed=None, health=None, angle=None, acceleration=None, turn_speed=None) -> None:
        super().__init__(color,image,rangee,cost, max_speed, max_health, x, y, speed, health, angle, acceleration, turn_speed)
        self.refueling_speed = 100 if refueling_speed is None else refueling_speed
        # self.image = self.load_icon("images/supply.png")
    
    def refuel(self):
        return self.refueling_speed
    
    def do_special(self):
        return self.refuel()
        
    def render(self,canvas)-> None:
            if (self.health > 0 ):
                if self.image:
                     canvas.blit(self.image, (self.x, self.y))
                # elif self.being_refueled:
                #     pygame.draw.circle(canvas, self.refueled_color, [self.x,self.y], 5)
                # elif self.being_attacked:
                #     pygame.draw.circle(canvas, self.attacked_color, [self.x,self.y], 5)
                else:
                    pygame.draw.circle(canvas, (0,255,0), [self.x,self.y], 5)
    