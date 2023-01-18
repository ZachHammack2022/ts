"""Contains player class and methods"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import numpy as np

class player():
    
    def __init__(self,radius,left,right,top,bottom,color) -> None:
        """ Initializes player object with no acceleration, velocity in position

            Args:
            x (double): x_coordinate
            y (double): y_coordinate
        """
        start_width = (right-left-21)
        start_height = (bottom-top-21)
        # store env bounds
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        # store player characteristics
        self.alive = 1.0
        self.color = color
        self.x = left+ 21+ np.random.random()*start_width
        self.y = top+ 21+ np.random.random()*start_height
        self.r = radius
        self.x_v = 0
        self.y_v = 0
        self.v_range = 20 # -15 or +15
        self.m = 1
        self.max_m = 5
        self.min_m = 1
        self.score = 0
        self._obs = np.array([self.normalize(left,right,self.x),self.normalize(top,bottom,self.y),self.x_v,self.y_v,self.alive,self.m])
    
        
    def update_velocities(self):
        
        # prepare velocities for normalization
        self.y_v +=1.5
        if self.x_v >self.v_range:
            self.x_v = self.v_range
        if self.x_v <-self.v_range:
            self.x_v = -self.v_range
        if self.y_v >self.v_range:
            self.y_v = self.v_range
        if self.y_v <-self.v_range:
            self.y_v = -self.v_range
            
    
    def update_position(self):

        self.x += self.x_v
        self.y += self.y_v
        self.y = min(self.bottom-self.r,self.y)
    
    def update_mass(self):
        if self.m > 1:
            self.m = max(self.m-0.1,1)
    
    def make_heavy(self):
        if self.m == 1:
            self.m = self.max_m
        
    
    def normalize_obs(self):
        
        x = self.normalize(self.left,self.right,self.x)
        y = self.normalize(self.top,self.bottom,self.y)
        x_v = self.normalize(-self.v_range,self.v_range,self.x_v)
        y_v = self.normalize(-self.v_range,self.v_range,self.y_v)
        m = self.normalize(self.min_m,self.max_m,self.m)
        
        self._obs = np.array([x,y,x_v,y_v,self.alive,m])
            
    def update(self)-> None:
        """_Update velocity and position values
        """
        
        self.update_velocities()
        self.update_position()
        self.update_mass()
        
    def render(self,canvas)-> None:
        pygame.draw.circle(canvas, (0,0,0), [self.x,self.y], self.r)
        pygame.draw.circle(canvas, self.color, [self.x,self.y], self.r-4*(self.m - self.min_m))

    
    def reset(self)->None:
        """Changes x or y vel to opposite direction

        Args:
            bounce (_type_): _description_
            vert (_type_): _description_
        """
        start_width = (self.right-self.left-21)
        start_height = (self.bottom-self.top-21)
        
        self.alive = 1.0
        self.x = self.left+ 21+ np.random.random()*start_width
        self.y = self.top+ 21+ np.random.random()*start_height
        self.x_v = 0
        self.y_v = 0
        self.m = 1
        
    
    def get_obs(self):
        self.normalize_obs()
        return self._obs
    
        
    def dies(self):
        """Set alive attribute to False upon death
        """
        self.alive = 0
    
    def move_up(self,force):
        self.y_v -= force/self.m
    
    def move_down(self,force):
        self.y_v += force/self.m
    
    def move_left(self,force):
        self.x_v -= force/self.m
    
    def move_right(self,force):
        self.x_v += force/self.m
        
    def normalize(self,low,high,val):
        return ((val - low)/(high-low)-0.5)*2

        