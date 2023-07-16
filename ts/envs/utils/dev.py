import numpy as np 
import gym
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
from ts.envs.utils.static_env import GridEnv
from ts.envs.utils.mechanics import env_collision, ship_in_range,ship_collision
from stable_baselines3 import PPO
from ts.envs.utils.ships.ship import Ship
from ts.envs.utils.ships.battleship import BattleShip
from ts.envs.utils.ships.supply_ship import SupplyShip

class DevEnv():
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    def __init__(self,render_mode = "human"):
        
        # grid limits (680x680 square)
        self.width = 680
        self.height = 680
        self.grid = GridEnv(0,self.width,0,self.height,color=(0,0,0))
        
        # dimensions to start ships between 
        self.boundary = 10
        self.left = self.grid.get_x_min()+ self.boundary
        self.right = self.grid.get_x_max()-self.boundary
        self.top = self.grid.get_y_min() + self.boundary
        self.bottom = self.grid.get_y_max() - self.boundary
        # Initialize ships
        s1_color = (255,102,102)
        s2_color = (0,102,204)
        self.s1 = SupplyShip(color = s1_color)
        self.s2 = BattleShip(color=s2_color)
        self.s3 = BattleShip(color=s2_color)
        self.s4 = BattleShip(color=s2_color)
        self.ships = [self.s1,self.s2,self.s3,self.s4]
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        self.window = None
        self.clock = None
        
    
    def fix_overlaps(self):
        # no need to check overlaps
        if len(self.ships)<2:
            return
        # Continue to reset ships until there are no overlaps
        overlap = True
        while overlap:
            overlap=False
            for i in range(len(self.ships)):
                ship1 = self.ships[i]
                assert isinstance(ship1,Ship)
                for j in range(i+1,len(self.ships)):
                    ship2 = self.ships[j]
                    assert isinstance(ship2,Ship)
                    if ship_collision(ship1,ship2):
                        ship1.reset()
                        ship2.reset()
                        overlap=True
                        
                        
    def check_collisions(self):
        # Each player checks each platform for collision
        for ship in self.ships:
            env_collision(ship, self.grid)
                
        # Each ship checks each ship for in_range
        for i in range(len(self.ships)):
            for j in range(i+1,len(self.ships)):
                ship_in_range(self.ships[i], self.ships[j])
            
        
    
    def reset(self):
        
        # Super.reset function omitted
        # reset ships
        for ship in self.ships:
            ship.reset()
      
        # Continue to reset ships until there are no overlaps
        self.fix_overlaps()
            
        # observation = self._get_obs(bad_agent=False)
        

        if self.render_mode == "human":
            self._render_frame()
            
        #info = self._get_info() not used or returned here
        # return observation
    
    # def make_action(self,agent,action):
    #     x = int(action)
    #     d = self._action_to_direction[x]
        
    #     # Update agent velocity
    #     agent.move_right(d[0]*self.force)
    #     agent.move_down(d[1]*self.force)
    #     if d[2]:
    #         agent.make_heavy()
    
    
    def step(self):
        
        # # if bad agent exists, bad agent acts based off of last obs
        # if self.bad_agent_exists:
        #     action2, _states = self.bad_agent.predict(self._get_obs(bad_agent=True))
        #     self.make_action(agent = self.p2,action = action2)
        
        
        # # Agent 1 acts no matter what
        # self.make_action(agent=self.p1,action = action1)
        for ship in self.ships:
            ship.move_randomly()
        
        for ship in self.ships:
            ship.update()

        self.check_collisions()
        
       
        # An episode is done if agent or enemy dies
        terminated =  False
        reward = -0.001
            
        observation = {}

        if self.render_mode == "human":
            self._render_frame()
        info = {}
        
        return observation, reward, terminated, info
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        
    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.width, self.height)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.width, self.height))
        canvas.fill((205, 240, 255))
        
        
        # Render agents
        for agent in self.ships:
            agent.render(canvas)
        
        # render environment objects
        # for object in self.env_objects:
        #     object.render(canvas)
    
        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
        )
        
    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    