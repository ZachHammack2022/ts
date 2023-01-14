"""Contains player class and methods"""
import pygame
import numpy as np

class player():
    
    def __init__(self,x,y,color) -> None:
        """ Initializes player object with no acceleration, velocity in position

            Args:
            x (double): x_coordinate
            y (double): y_coordinate
        """
        left = 100
        right = 580
        top = 135
        bottom = 420
        start_width = (right-left-21)
        start_height = (bottom-top-21)
        
        self.heavy = False
        self.alive = True
        self.color = color
        self.x = left+ 21+ np.random.random()*start_width
        self.y = top+ 21+ np.random.random()*start_height
        self.r = 20
        self.x_v = 0
        self.y_v = 0
        self.x_a = 0
        self.y_a = 0
        self.m = 1
        self.sx = x
        self.opp_score = 0
        self.score = 0
        self._obs_space = {
            "x": self.x,
            "y": self.y,
            "x_v": self.x_v,
            "y_v" : self.y_v
        }
       
    def update(self,score)-> None:
        """_Update velocity and position values
        """
        #assert(self.alive == True)
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
        # # for testing
        # if self.x <-10 or self.x >680 or self.y<-10 or self.y >480:
        #      self.reset(self.sx,200)
        
    def render(self,canvas)-> None:
        pygame.draw.circle(canvas, self.color, [self.x,self.y], self.r)
    
    def reset(self)->None:
        """Changes x or y vel to opposite direction

        Args:
            bounce (_type_): _description_
            vert (_type_): _description_
        """
        left = 100
        right = 580
        top = 135
        bottom = 420
        start_width = (right-left-21)
        start_height = (bottom-top-21)
        
        self.heavy = False
        self.alive = 1
        self.x = left+ 21+ np.random.random()*start_width
        self.y = top+ 21+ np.random.random()*start_height
        self.r = 20
        self.x_v = 0
        self.y_v = 0
        self.x_a = 0
        self.y_a = 0
        self.m = 1
        self.opp_score +=1
    
        
    def dies(self):
        """Set alive attribute to False upon death
        """
        self.alive = 0

        