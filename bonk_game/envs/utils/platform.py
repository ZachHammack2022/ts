"""Contains platform class and methods."""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class platform():
    
    def __init__(self,x1,x2,y1,y2,color,kill) -> None:
        """ Initializes player object with no acceleration, velocity in position

            Args:
            x (double): x_coordinate
            y (double): y_coordinate
        """
        
        self.kill = kill
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.color = color
    
    def render(self,canvas)->None:
        """Render rectangular platform to canvas

        
        Args:
            canvas (_type_): pygame canvas
            Rect(left, top, width, height) -> Rect
            
        """
        rect = pygame.Rect(self.x1,self.y1,abs(self.x2-self.x1),abs(self.y2-self.y1))
        
        pygame.draw.rect(canvas, self.color, rect)
        
    