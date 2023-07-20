# """Contains player class and methods"""
# import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
# import numpy as np
import math
import random

class Ship():
    
    def __init__(self,color,image = None,rangee=None,cost=None,max_speed=None,max_health=None,x=None,y=None,speed=None,health=None,angle=None, acceleration=None,turn_speed=None,) -> None:
        """ 
        Initializes ship object.
        """
        self.r = 5 # ships are the same size
        self.color = color
        
        self.x = random.randint(10, 500) if x is None else x
        self.y = random.randint(10, 500) if y is None else y
        self.angle = random.randint(0,360) if angle is None else angle
        self.acceleration = .1 if acceleration is None else acceleration
        self.turn_speed = .1 if turn_speed is None else turn_speed #how quickly can it change angle
        self.speed = 0 if speed is None else speed
        self.max_health = 100 if max_health is None else max_health
        self.health = self.max_health if health is None else health
        self.max_speed = 5 if max_speed is None else max_speed
        self.cost=10 if cost is None else cost
        self.range=20 if rangee is None else rangee
        self.image=image
        self.being_refueled = False
        self.being_attacked = False
        self.refueled_color = (40,40,40)
        self.attacked_color = (0,100,100)
        
    
    def get_coordinates(self):
        return [self.x,self.y]
    
    def get_health(self):
        return self.health
    
    def get_cost(self):
        return self.cost
    
    def get_range(self):
        return self.range
    
    def get_radius(self):
        return self.r
    
    def hit_edge(self):
        self.acceleration=0
        self.speed=0
    
    def set_x(self,x):
        self.x = x
        
    def set_y(self,y):
        self.y = y
        
    def accelerate(self):
        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed
    
    def decelerate(self):
        self.speed -= self.acceleration
        if self.speed < 0:
            self.speed = 0

    def turn_left(self):
        self.angle += self.turn_speed

    def turn_right(self):
        self.angle -= self.turn_speed
    
    def move_randomly(self):
        action = random.randint(0, 5)
        if action ==0:
            self.accelerate()
        elif action == 1:
            self.decelerate()
        elif action == 2:
            self.turn_left()
        elif action == 3:
            self.turn_right()
        else:
            # Do nothing if action is 6,7
            pass
    
    def do_special(self):
        print("Doing special.")
        
        
    def update(self):
        # Update position based on speed and angle
        radian_angle = math.radians(self.angle)
        self.x += math.sin(radian_angle) * self.speed
        self.y += math.cos(radian_angle) * self.speed
    
    
    def lose_health(self,health):
        self.health -= health
        self.health = max(0,self.health)
        
    def gain_health(self,health):
        self.health += health
        self.health = min(self.health,self.max_health)
    
    def set_attacked(self):
        self.being_attacked = True
    
    def set_refueled(self):
        self.being_refueled = True
    
    def set_not_refueled(self):
        self.being_refueled = False
    
    def load_icon(self,path,width=None,height=None):
         # Load the PNG image
        image = pygame.image.load(path)

        # Define the desired width and height
        width = 60 if width is None else width
        height = 60 if height is None else height

        # Resize,rotate the image
        resized_image = pygame.transform.scale(image, (width, height))
        rotated_image = pygame.transform.rotate(resized_image,self.angle)
        return rotated_image

    def render(self,canvas)-> None:
            if (self.health > 0 ):
                if self.image:
                     canvas.blit(self.image, (self.x, self.y))
                elif self.being_refueled:
                    pygame.draw.circle(canvas, self.refueled_color, [self.x,self.y], 5)
                elif self.being_attacked:
                    pygame.draw.circle(canvas, self.attacked_color, [self.x,self.y], 5)
                else:
                    pygame.draw.circle(canvas, self.color, [self.x,self.y], 5)

    def reset(self,x=None,y=None,speed=None,health=None,angle=None) -> None:
        """ 
        Resets ship object.
        """
        
        self.x = random.randint(10, 360) if x==None else x
        self.y = random.randint(10, 360) if y==None else y
        self.angle = random.randint(0,360) if angle==None else angle
        self.speed = 0 if speed==None else speed
        self.health = self.max_health if health==None else health
        
    
    # def get_obs(self):
    #     self.normalize_obs()
    #     return self._obs
    
    
        
    # def normalize(self,low,high,val):
    #     return ((val - low)/(high-low)-0.5)*2
    
     
    # def normalize_obs(self):
        
    #     x = self.normalize(self.left,self.right,self.x)
    #     y = self.normalize(self.top,self.bottom,self.y)
    #     x_v = self.normalize(-self.v_range,self.v_range,self.x_v)
    #     y_v = self.normalize(-self.v_range,self.v_range,self.y_v)
    #     m = self.normalize(self.min_m,self.max_m,self.m)
        
    #     self._obs = np.array([x,y,x_v,y_v,self.alive,m])
    
    
     # self.score = 0
        # self._obs = np.array([self.normalize(left,right,self.x),self.normalize(top,bottom,self.y),self.x_v,self.y_v,self.alive,self.m])

        