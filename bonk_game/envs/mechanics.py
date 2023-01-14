"""This file includes all physics based functions to diplatform gameplay."""
import math



def env_collision_game(agent, platform)->bool:
    """_summary_
    This function is called when testing if an an agent collides with 
    a platform in-game. 

    Args:
        agent (_type_ player): An moving agent in the game
        platform (_type_ platform): A stationary platform

    Returns:
        bool: Whether to pause due to a reset (to allow player to see
        where new starting point is)
    """
    collision = env_collision(agent,platform)
    if collision:
        if platform.kill:
            agent.reset()
            return True
        else:
            handle_env_collision(agent,platform);
    return False
    

def env_collision_gym(agent, platform)->None:
    """_summary_
    This function is called when testing if an an agent collides with 
    a platform in the gym env. 

    Args:
        agent (_type_ player): An moving agent in the game
        platform (_type_ platform): A stationary platform

    """
    collision = env_collision(agent,platform)
    if collision and platform.kill:
        agent.dies()
    elif collision:
        handle_env_collision(agent,platform);
    
    


def env_collision(agent, platform)->bool:
    """_summary_
    Math behind determining if agent colides with platform in-game.

    Args:
        agent (_type_ player): An moving agent in the game
        platform (_type_ platform): A stationary platform

    Returns:
        bool: if a collision occurs between agent and platform
    """
    cx,cy,radius = agent.x,agent.y,agent.r
    rx,ry,rw,rh  = platform.x1,platform.y1,abs(platform.x2-platform.x1),abs(platform.y2-platform.y1)
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

def handle_env_collision(agent,platform)->None:
    """_summary_
    Bounces agent off one of the horizontal platforms
    (Does not work for vertical platforms or slanted platforms)

    Args:
        agent (_type_ player): An moving agent in the game
        platform (_type_ platform): A stationary platform
    """
    bounce = 0.8
    ## to check for collision
    # floor.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)) 
    agent.y_a = 0
    agent.y_v = bounce *-(agent.y_v);
    if platform.y1< 200:
        agent.y = 135+ agent.r +0.01
    else:
        agent.y = 420 - agent.r - 1
            
        

def player_collision(a1,a2)->None:
    """
    Determines if 2 agents collide

    Args:
        a1 (_type_ player): An moving agent in the game
        a2 (_type_ player): An moving agent in the game
    """
    cx1,cx2,cy1,cy2 = a1.x,a2.x,a1.y,a2.y
    d = math.sqrt(math.pow(cx1 - cx2, 2) + math.pow(cy1 - cy2, 2)); 
    if d < (a1.r+ a2.r):
        handle_player_collision(a1,a2,d)
    
    
def handle_player_collision(a1,a2,d)->None:
    """
    Handles if 2 agents collide

    Args:
        a1 (_type_ player): An moving agent in the game
        a2 (_type_ player): An moving agent in the game
    """
    cx1,cx2,cy1,cy2 = a1.x,a2.x,a1.y,a2.y
    nx = ((cx2-cx1) / d)
    ny = ((cy2-cy1) / d)
    p = 2 * (a1.x_v * nx + a1.y_v * ny - a2.x_v * nx - a2.y_v * ny) / (a1.m + a2.m);
    a1.x_v = a1.x_v - p * a1.m * nx
    a1.y_v = a1.y_v - p * a1.m * ny
    a2.x_v = a2.x_v+ p * a2.m * nx
    a2.y_v = a2.y_v + p * a2.m * ny
    

    

   
