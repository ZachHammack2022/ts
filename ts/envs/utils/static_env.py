# """Contains player class and methods"""
# import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class GridEnv():
    
    def __init__(self,x_min,x_max,y_min,y_max,color) -> None:
        """ Initializes static grid object.
        """
      
        # store grid characteristics
        self.x1 = x_min
        self.y1 = y_min
        self.x2 = x_max
        self.y2 = y_max
        self.color = color
        
    def get_x_min(self):
        return self.x1

    def get_x_max(self):
        return self.x2
    
    def get_y_min(self):
        return self.y1

    def get_y_max(self):
        return self.y2  
    
    def get_color(self):
        return self.color     