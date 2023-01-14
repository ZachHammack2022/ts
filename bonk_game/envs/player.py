"""Contains player class and methods"""
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
        self.x_a = 0
        self.y_a = 0
        self.m = 1
        self.opp_score = 0
        self.score = 0
        self._obs = np.array([self.normalize(left,right,self.x),self.normalize(top,bottom,self.y),self.x_v,self.y_v,self.alive])
       
    def update(self,score)-> None:
        """_Update velocity and position values
        """
        v_constant = 0.8
        p_constant = 0.8
        g_constant = .4
        self.x_v += v_constant*self.x_a
        self.y_v += v_constant*self.y_a + g_constant
        # prepare velocities for normalization
        if self.x_v >15:
            self.x_v = 15
        if self.x_v <-15:
            self.x_v = -15
        if self.y_v >15:
            self.y_v = 15
        if self.y_v <-15:
            self.y_v = -15
            
        
        self.x+= p_constant*self.x_v
        self.y += p_constant*self.y_v
        self.y = min(420-self.r,self.y)
        self.score = score
        
        self._obs = np.array([self.normalize(left,right,self.x),self.normalize(top,bottom,self.y),self.x_v,self.y_v,self.alive])
        # # for testing
        # if self.x <-10 or self.x >680 or self.y<-10 or self.y >480:
        #      self.reset(self.sx,200)
        
    def render(self,canvas)-> None:
        pygame.draw.circle(canvas, self.color, [self.x,self.y], self.r)
    
    def reset(self,left,right,top,bottom)->None:
        """Changes x or y vel to opposite direction

        Args:
            bounce (_type_): _description_
            vert (_type_): _description_
        """
        start_width = (right-left-21)
        start_height = (bottom-top-21)
        
        self.heavy = False
        self.alive = 1.0
        self.x = left+ 21+ np.random.random()*start_width
        self.y = top+ 21+ np.random.random()*start_height
        self.x_v = 0
        self.y_v = 0
        self.x_a = 0
        self.y_a = 0
        self.m = 1
        self.opp_score +=1
        x = self.normalize(left,right,self.x)
        y = self.normalize(bottom,top,self.y)
        
        self._obs = np.array([x,y,self.x_v,self.y_v,self.alive])
    
        
    def dies(self):
        """Set alive attribute to False upon death
        """
        self.alive = 0
        
    def normalize(self,low,high,val):
        return ((val - low)/(high-low)-0.5)*2

        