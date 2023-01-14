"""This file includes all physics based functions to direct gameplay."""
import math

## for gameplay
def env_collision_game(circle, rect)->None:
    collision = env_collision(circle,rect)
    if collision:
        if rect.kill:
            circle.reset(circle.sx,200)
        else:
            handle_env_collision(circle,rect);
    
    
def env_collision_gym(circle, rect)->None:
    collision = env_collision(circle,rect)
    if collision and rect.kill:
        circle.dies()
    elif collision:
        handle_env_collision(circle,rect);
    
    


def env_collision(circle, rect)->bool:
    cx,cy,radius = circle.x,circle.y,circle.r
    rx,ry,rw,rh  = rect.x1,rect.y1,abs(rect.x2-rect.x1),abs(rect.y2-rect.y1)
    #temporary variables to set edges for testing
    test_x = cx;
    test_y = cy;

    #// which edge is closest?
    if (cx < rx):         
        test_x = rx;      # test left edge
    elif (cx > rx+rw):
        test_x = rx+rw;   # right edge
    if (cy < ry):
        test_y = ry;      # top edge
    elif (cy > ry+rh):
        test_y = ry+rh;   # bottom edge

    #// get distance from closest edges
    dist_x = cx-test_x;
    dist_y = cy-test_y
    distance = math.sqrt( (dist_x**2) + (dist_y**2) );

    #// if the distance is less than the radius, collision!
    if (distance <= radius):
        return True

def handle_env_collision(user,rect)->None:
    bounce = 0.8
    ## to check for collision
    # floor.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) 
    user.y_a = 0
    user.y_v = bounce *-(user.y_v);
    if rect.y1< 200:
        user.y = 135+ user.r +0.01
    else:
        user.y = 420 - user.r - 1
            
        

def player_collision(p1,p2)->None:
    cx1,cx2,cy1,cy2 = p1.x,p2.x,p1.y,p2.y
    d = math.sqrt(math.pow(cx1 - cx2, 2) + math.pow(cy1 - cy2, 2)); 
    if d < (p1.r+ p2.r):
        handle_player_collision(p1,p2)
    
    
def handle_player_collision(p1,p2)->None:
    cx1,cx2,cy1,cy2 = p1.x,p2.x,p1.y,p2.y
    d = math.sqrt(math.pow(cx1 - cx2, 2) + math.pow(cy1 - cy2, 2)); 
    # nx = 0 if d == 0 else (cx2-cx1 / d)
    # ny = 0 if d == 0 else (cy2-cy1 / d)
    nx = ((cx2-cx1) / d)
    ny = ((cy2-cy1) / d)
    p = 2 * (p1.x_v * nx + p1.y_v * ny - p2.x_v * nx - p2.y_v * ny) / (p1.m + p2.m);
    p1.x_v = p1.x_v - p * p1.m * nx
    p1.y_v = p1.y_v - p * p1.m * ny
    p2.x_v = p2.x_v+ p * p2.m * nx
    p2.y_v = p2.y_v + p * p2.m * ny
    # set a to 0
    p1.a_x = 0
    p1.a_y = 0
    p2.a_x = 0
    p2.a_y = 0;
    
def update(self,keystrokes)->None:
    """_summary_

    Args:
        keystrokes (double array): Values for if key was pressed or not
    """
    assert(self.alive == True)
    a_constant = 0.2
    v_constant = 0.3
    p_constant = 1
    up,down,left,right, heavy = keystrokes[0],keystrokes[1],keystrokes[2], keystrokes[3],keystrokes[4]
    self.x_a += a_constant*(left+right)
    self.y_a += a_constant*(up+down)
    self.x_v += v_constant*self.x_a
    self.y_v += v_constant*self.y_a
    self.x_p+= p_constant*self.x_v
    self.y_p += p_constant*self.y_v
    

    

   
