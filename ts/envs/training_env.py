import numpy as np 
import gym
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
from ts.envs.utils.static_env import GridEnv
from ts.envs.utils.mechanics import env_collision, ship_in_range,ship_collision
from stable_baselines3 import PPO
from ts.envs.utils.ships.ship import Ship
from ts.envs.utils.ships.battleship import BattleShip
from ts.envs.utils.ships.supply_ship import SupplyShip

class TsEnv(gym.Env):
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    def __init__(self,render_mode = None):
        
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
        numships = random.randint(3, 9)
        self.free_ships = []
        self.ships = [self.s1]
        for _ in range(numships):
            ship = BattleShip(color=s1_color)
            self.free_ships.append(ship)
            self.ships.append(ship)
        self.step_count= 0
        
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        
        
        # Define Observation space (up to 10 friendlys, each w coordinates, health, cost, battlepower)
        self.observation_space = gym.spaces.Box(-1,1,shape = (50,),dtype = np.float64)
        
        # Define Action Space 
        self.action_space = gym.spaces.Discrete(9)


           # Map action to movement (x,y,heavy action)
        self._action_to_direction = {
            0: np.array([0, 0]),
            1: np.array([0, 1]),
            2: np.array([0, 2]),
            3: np.array([1,0]),
            4: np.array([1, 1]),
            5: np.array([1, 2]),
            6: np.array([2, 0]),
            7: np.array([2, 1]),
            8: np.array([2, 2]),
        }
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
                        
    def get_observations(self):               
        observations = []
        for i in range(10):
            if i < len(self.ships):
                ship = self.ships[i]
                assert isinstance(ship,Ship)
                x,y = ship.get_coordinates()
                nx = self.normalize(self.grid.get_x_min(),self.grid.get_x_max(),x)
                ny = self.normalize(self.grid.get_y_min(),self.grid.get_y_max(),y)
                health = ship.get_health()
                nh = self.normalize(0,500,health)
                cost = ship.get_cost()
                nc = self.normalize(0,100,cost)
                battlepower = 0
                if isinstance(ship,BattleShip):
                    battlepower = ship.attack()
                nb = self.normalize(0,100,battlepower)
                observations.append([nx,ny,nh,nc,nb])
            else:
                observations.append([0,0,0,0,0])

        concatenated_obs = np.concatenate(observations, axis=0)
        flattened_obs = concatenated_obs.flatten()
        return flattened_obs
    
    def normalize(self,low,high,val):
        return ((val - low)/(high-low)-0.5)*2                
                        
    def check_collisions(self):
        # Each player checks each platform for collision
        for ship in self.ships:
            env_collision(ship, self.grid)
                
        # Each ship checks each ship for in_range
        for i in range(len(self.ships)):
            for j in range(i+1,len(self.ships)):
                ship_in_range(self.ships[i], self.ships[j])
            
        
    
    def reset(self,seed1 = None, options=None):
        
        for ship in self.ships:
            ship.reset()
        
        self.fix_overlaps()        

        if self.render_mode == "human":
            self._render_frame()
        
        observation = self.get_observations()
            
        return observation
    
    def make_action(self,ship,action):
        assert isinstance(ship,Ship)
        x = int(action)
        d = self._action_to_direction[x]
        
        # Update agent velocity
        if d[0] == 0:
            ship.accelerate()
        elif d[0]==1:
            ship.decelerate()
        
        if d[1] == 0:
            ship.turn_left()
        elif d[1]==1:
            ship.turn_right()
        
        
    
    
    def step(self,action1):
        
        # # if bad agent exists, bad agent acts based off of last obs
        # if self.bad_agent_exists:
        #     action2, _states = self.bad_agent.predict(self._get_obs(bad_agent=True))
        #     self.make_action(agent = self.p2,action = action2)
        
        
        # Agent 1 acts no matter what
        self.make_action(ship=self.s1,action = action1)
        # for ship in self.free_ships:
        #     ship.move_randomly()
        
        for ship in self.ships:
            ship.set_not_refueled()
            
        self.check_collisions()
        
        terminated= True
        for ship in self.ships:
            if ship.get_health()<=0:
                continue
            ship.update()
            if ship.get_health() > 0:
                terminated = False
        
        for ship in self.free_ships:
            assert isinstance(ship,Ship)
            ship.lose_health(0.5)
            # print(ship.get_health())
        
        
       
        # An episode is done if agent or enemy dies
        reward = -0.01
        self.step_count +=1
        if self.step_count==499:
            terminated=True
        if terminated:
            for ship in self.free_ships:
                if isinstance(ship,BattleShip):
                    reward += ((ship.attack()*ship.get_health())!=0)/len(self.free_ships)
                else:
                    reward -= 1
        observation = self.get_observations()

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
        # canvas.fill((205, 240, 255))
        canvas.fill((255, 255, 255))
        
        # Render agents
        for agent in self.ships:
            agent.render(canvas)
        
    
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

    