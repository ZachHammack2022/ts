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
        self.heavy = False
        self.alive = True
        self.color = color
        self.x = left+ 21+ np.random.random()*start_width
        self.y = top+ 21+ np.random.random()*start_height
        self.r = radius
        self.x_v = 0
        self.y_v = 0
        self.v_range = 5 # -15 or +15
        self.x_a = 0
        self.y_a = 0
        self.m = 1
        self.max_a = 0.5
        self.score = 0
        self._obs = np.array([self.normalize(left,right,self.x),self.normalize(top,bottom,self.y),self.x_v,self.y_v,self.alive])
    
    def update_acceleration(self):   
        g_constant = .1
        if self.x_a > self.max_a:
            self.x_a = self.max_a
        elif self.x_a < -self.max_a:
            self.x_a = -self.max_a
        if self.y_a > self.max_a:
            self.y_a = self.max_a
        elif self.y_a < -self.max_a:
            self.y_a = -self.max_a
        self.y_a += g_constant
        
    def update_velocities(self):
        
        # update velocities according to acceleration
        self.x_v += self.x_a
        self.y_v += self.y_a
        # prepare velocities for normalization
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
    
    def normalize_obs(self):
        
        x = self.normalize(self.left,self.right,self.x)
        y = self.normalize(self.top,self.bottom,self.y)
        x_v = self.normalize(-self.v_range,self.v_range,self.x_v)
        y_v = self.normalize(-self.v_range,self.v_range,self.y_v)
        
        self._obs = np.array([x,y,x_v,y_v,self.alive])
            
    def update(self)-> None:
        """_Update velocity and position values
        """
        
        self.update_acceleration()
        self.update_velocities()
        self.update_position()
        self.normalize_obs()
        
    def render(self,canvas)-> None:
        pygame.draw.circle(canvas, self.color, [self.x,self.y], self.r)
    
    def reset(self)->None:
        """Changes x or y vel to opposite direction

        Args:
            bounce (_type_): _description_
            vert (_type_): _description_
        """
        start_width = (self.right-self.left-21)
        start_height = (self.bottom-self.top-21)
        
        self.heavy = False
        self.alive = 1.0
        self.x = self.left+ 21+ np.random.random()*start_width
        self.y = self.top+ 21+ np.random.random()*start_height
        self.x_v = 0
        self.y_v = 0
        self.x_a = 0
        self.y_a = 0
        self.m = 1
        x = self.normalize(self.left,self.right,self.x)
        y = self.normalize(self.top,self.bottom,self.y)
        
        self._obs = np.array([x,y,self.x_v,self.y_v,self.alive])
    
        
    def dies(self):
        """Set alive attribute to False upon death
        """
        self.alive = 0
        
    def normalize(self,low,high,val):
        return ((val - low)/(high-low)-0.5)*2

        