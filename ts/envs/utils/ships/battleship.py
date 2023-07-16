# import os
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from ts.envs.utils.ships.ship import Ship
import math
import pygame

class BattleShip(Ship):
    
    def __init__(self, color,image=None,rangee=None,cost=None,battle_power=None, max_speed=None, max_health=None, x=None, y=None, speed=None, health=None, angle=None, acceleration=None, turn_speed=None) -> None:
        super().__init__(color,image,rangee,cost, max_speed, max_health, x, y, speed, health, angle, acceleration, turn_speed)
        self.battle_power = 10 if battle_power is None else battle_power
        self.image = self.load_icon("images/battleship.png")
        
    
    def attack(self):
        return self.battle_power
    
    def do_special(self):
        return self.attack()
    
    