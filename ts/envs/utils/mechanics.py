"""This file includes all physics based functions to direct gameplay."""
import math
from ts.envs.utils.ships.ship import Ship
from ts.envs.utils.ships.battleship import BattleShip
from ts.envs.utils.ships.supply_ship import SupplyShip
from ts.envs.utils.static_env import GridEnv

def env_collision(ship, env)->bool:
    """_summary_
    Math behind determining if ship colides with env in-game.

    Args:
        ship (_type_ player): An moving ship in the game
        env (_type_ env): A stationary env
    """
    assert isinstance(ship,Ship)
    assert type(env)==GridEnv
    x,y = ship.get_coordinates()
    radius = ship.get_radius()
    x_min,y_min,x_max,y_max  = env.get_x_min(), env.get_y_min(),env.get_x_max(), env.get_y_max()
    
    # Check if the ship is outside the x boundaries and reset if necessary
    if (x - radius < x_min):
        ship.set_x(x_min + radius+2)
    elif (x + radius > x_max):
        ship.set_x(x_max - radius-2)

    # Check if the ship is outside the y boundaries and reset if necessary
    if (y - radius < y_min):
        ship.set_y(y_min + radius+2)
    elif (y + radius > y_max):
        ship.set_y(y_max - radius-2)
        
def get_distance(s1,s2):
    assert isinstance(s1,Ship)
    assert isinstance(s2,Ship) 
    return math.dist(s1.get_coordinates(),s2.get_coordinates())
            
        

def ship_collision(s1,s2)->bool:
    """
    Determines if 2 ships collide

    Args:
        a1 (_type_ player): An moving ship in the game
        a2 (_type_ player): An moving ship in the game
    """
    assert isinstance(s1,Ship)
    assert isinstance(s2,Ship)
    if get_distance(s1,s2) < (s1.get_radius()+ s2.get_radius()):
        return True
    
    
def ship_in_range(s1,s2)->None:
    """
    Checks, handles if 2 ships are in range

    Args:
        a1 (_type_ player): An moving ship in the game
        a2 (_type_ player): An moving ship in the game
    """
    assert isinstance(s1,Ship)
    assert isinstance(s2,Ship)
    distance = get_distance(s1,s2)
    d1 = distance + s1.get_radius() -s2.get_radius()
    if (d1 < s1.get_range()):
        if (s1.color == s2.color and isinstance(s1,SupplyShip)):
            s2.gain_health(s1.refuel())
            s2.set_refueled()
        elif(s1.color != s2.color and isinstance(s1,BattleShip)):
            s2.lose_health(s1.attack())
        
    
    d2 = distance + s2.get_radius() -s1.get_radius()
    if (d2 < s2.get_range()):
        if (s1.color == s2.color and isinstance(s2,SupplyShip)):
            s1.gain_health(s2.refuel())
            
        elif(s1.color != s2.color and isinstance(s2,BattleShip)):
            s1.lose_health(s2.attack())
    
    
    
    
    
    