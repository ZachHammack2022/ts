import numpy as np 
import cv2 
#import gymnasium as gym
import gym
import matplotlib.pyplot as plt
from gym import Env, spaces
import time
import pygame
from bonk_game.envs.player import player
from bonk_game.envs.platform import platform
from bonk_game.envs.mechanics import env_collision_gym,player_collision

class BonkEnv(gym.Env):
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 20}
    def __init__(self,render_mode = None):
        self.width = 680
        self.height = 480 
        # Initialize players
        p1_color = (255,102,102)
        p2_color = (0,102,204)
        self.p1 = player(200,200,p1_color)
        self.p2 = player(400,200,p2_color)
        self.players = [self.p1,self.p2]
    

    
        # Initialize platforms
        ceiling_color = (255,204,204)
        wall_color = (32,32,32)
        self.floor = platform(100,580,420,435,ceiling_color,kill = False)
        self.left_wall = platform(80,100,115,435,wall_color,kill = True)
        self.right_wall = platform(580,600,115,435,wall_color,kill = True)
        self.ceiling = platform(100,580,115,135,ceiling_color,kill = False)
        self.env_objects = [self.floor,self.left_wall,self.right_wall,self.ceiling]
        
        
        self.observation_space = gym.spaces.Box(-1,1,shape = (10,),dtype = np.float64)
        
        # We have 8 actions, corresponding to "right", "up", "left", "down", right up right down, left up left down
        # should be int 0-7 (discrete)
        #self.action_space = 
        self.action_space = gym.spaces.Discrete(8)
        
        """
        The following dictionary maps abstract actions from `self.action_space` to
        the direction we will walk in if that action is taken.
        I.e. 0 corresponds to "right", 1 to "up" etc.
        """
        self._action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
            4: np.array([1, 1]),
            5: np.array([1, -1]),
            6: np.array([-1, 1]),
            7: np.array([-1, -1])
        }
        
        
        
        
        
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
        
    def _get_obs(self):
        return np.concatenate((self._agent_obs,self._enemy_obs),axis = 0)
    
    def normalize(self,low,high,val):
        return ((val - low)/(high-low)-0.5)*2
        
    
    def reset(self,  seed1 = None, options=None):
        # We need the following line to seed self.np_random
        #seed=seed1
        #super().reset(seed = seed1)

        # Choose the agent's location uniformly at random
        #self._agent_location = self.np_random.integers(0, self.size, size=2, dtype=int)
        
        x = self.normalize(100,580,(121+ np.random.random()*(499-121)))
        y = self.normalize(135,520,200)
        x_v,y_v = 0.0,0.0
        alive = 1.0
        data = [x,y,x_v,y_v,alive]
        self._agent_obs = np.array(data)
        x = self.normalize(100,580,(121+ np.random.random()*(499-121)))
        y = self.normalize(135,520,200)
        x_v,y_v = 0.0,0.0
        alive = 1.0
        data = [x,y,x_v,y_v,alive]
        self._enemy_obs = np.array(data)
        
    

        # We will sample the target's location randomly until it does not coincide with the agent's location
        while abs(self._agent_obs[0]*480-self._enemy_obs[0]*480)<25:
            self._enemy_obs[0] = self.normalize(100,580,(121+ np.random.random()*(499-121)))
            

        observation = self._get_obs()
        #info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()
        return observation
    
    
    def step(self, action):
        # Map the action (element of {0,1,2,3}) to the direction we walk in
        # not sure why i need to cast this from np int to int
        x = int(action)
        direction = self._action_to_direction[x]
        # Update agent velocity
        self._agent_obs[2]+= direction[0]
        self._agent_obs[3] += direction[1]
        self.p1.x_v = self._agent_obs[2]
        self.p2.y_v = self._agent_obs[3]
        for env_obj in self.env_objects:
            env_collision_gym(self.p1, env_obj)
            env_collision_gym(self.p2, env_obj)
        player_collision(self.p1, self.p2)
        self.p1.update(self.p2.opp_score)
        self.p2.update(self.p1.opp_score)
        
        
        
        ## update observations before passing
        self._agent_obs[0] = self.normalize(100,580,self.p1.x)
        self._agent_obs[1] = self.normalize(135,520,self.p1.y)
        self._agent_obs[2] = self.normalize(-15,15,self.p1.x_v)
        self._agent_obs[3] = self.normalize(-15,15,self.p1.y_v)
        
        self._enemy_obs[0] = self.normalize(100,580,self.p2.x)
        self._enemy_obs[1] = self.normalize(135,520,self.p2.y)
        self._enemy_obs[2] = self.normalize(-15,15,self.p2.x_v)
        self._enemy_obs[3] = self.normalize(-15,15,self.p2.y_v)
        
        
        # An episode is done if agent or enemy dies
        terminated = not self.p1.alive or not self.p2.alive
        reward = -0.01
        if terminated:
            if self.p1.alive:
                reward = 1
            else:
                reward = -1 # Binary sparse rewards
            
        observation = self._get_obs()
        #info = self._get_info()

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
        canvas.fill((255, 255, 255))
        # pix_square_size = (
        #     self.window_size / self.size
        # )  # The size of a single grid square in pixels
        
        # still need to draw platforms
        self.p1.render(canvas)# 20 is self.r
        self.p2.render(canvas) 
        
        # render walls, ceiling, floor
        for object in self.env_objects:
            object.render(canvas)
    
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
        
        
        
        
        
        
        
        
        
        
        
        # super(Bonk, self).__init__()
        

        
        # # Define a 2-D observation space
        # self.observation_shape = (600, 800, 3)
        # self.observation_space = spaces.Box(low = np.zeros(self.observation_shape), 
        #                                     high = np.ones(self.observation_shape),
        #                                     dtype = np.float16)
    
        
        # # Define an action space ranging from 0 to 4
        # self.action_space = spaces.Discrete(6,)
                        
        # # Create a canvas to render the environment images upon 
        # self.canvas = np.ones(self.observation_shape) * 1
        
        # # Define elements present inside the environment
        # self.elements = []
        
        # # Maximum fuel chopper can take at once
        # self.max_fuel = 1000

        # # Permissible area of helicper to be 
        # self.y_min = int (self.observation_shape[0] * 0.1)
        # self.x_min = 0
        # self.y_max = int (self.observation_shape[0] * 0.9)
        # self.x_max = self.observation_shape[1]
        