import numpy as np 
import gym
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
from bonk_game.envs.utils.player import player
from bonk_game.envs.utils.platform import platform
from bonk_game.envs.utils.mechanics import env_collision_gym,player_collision
from stable_baselines3 import PPO

class BonkEnv(gym.Env):
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    def __init__(self,render_mode = None):
        
        # dimensions of screen
        self.width = 680
        self.height = 480 
        # dimensions to start players between
        self.left = 100
        self.right = 580
        self.top = 135
        self.bottom = 420
        self.r = 20
        
        # Initialize players
        p1_color = (255,102,102)
        p2_color = (0,102,204)
        self.p1 = player(self.r,self.left,self.right,self.top,self.bottom,p1_color)
        self.p2 = player(self.r,self.left,self.right,self.top,self.bottom,p2_color)
        self.players = [self.p1,self.p2]
        self.force = 2
    
        # Initialize platforms
        ceiling_color = (255,204,204)
        wall_color = (32,32,32)
        
        self.floor = platform(self.left,self.width-self.left,self.bottom,self.bottom+15,ceiling_color,kill = False)
        self.left_wall = platform(self.left-20,self.left,self.top-20,self.bottom+15,wall_color,kill = True)
        self.right_wall = platform(self.right,self.right+20,self.top-20,self.bottom+15,wall_color,kill = True)
        self.ceiling = platform(self.left,self.right,self.top-20,self.top,ceiling_color,kill = False)
        self.env_objects = [self.floor,self.left_wall,self.right_wall,self.ceiling]
        
        # Define Observation space 
        self.observation_space = gym.spaces.Box(-1,1,shape = (12,),dtype = np.float64)
        
        # Define Action Space
        self.action_space = gym.spaces.Discrete(16)
        
          # Map action to movement (x,y,heavy action)
        self._action_to_direction = {
            0: np.array([1, 0,0]),
            1: np.array([0, 1,0]),
            2: np.array([-1, 0,0]),
            3: np.array([0, -1,0]),
            4: np.array([1, 1,0]),
            5: np.array([1, -1,0]),
            6: np.array([-1, 1,0]),
            7: np.array([-1, -1,1]),
            8: np.array([1, 0,1]),
            9: np.array([0, 1,1]),
            10: np.array([-1, 0,1]),
            11: np.array([0, -1,1]),
            12: np.array([1, 1,1]),
            13: np.array([1, -1,1]),
            14: np.array([-1, 1,1]),
            15: np.array([-1, -1,1]),
        }
        
        # Load bad agent if it exists
        self.bad_agent = 0
        self.bad_agent_exists = 0
        path = f"./agents/bad.zip"
        if (os.path.exists(path)):
            file_name = f"./agents/bad"
            self.bad_agent = PPO.load(file_name)
            self.bad_agent_exists = 1
     
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
        
    def _get_obs(self,bad_agent):
        if bad_agent:
            return np.concatenate((self.p2.get_obs(),self.p1.get_obs()),axis = 0)
        else:
            return np.concatenate((self.p1.get_obs(),self.p2.get_obs()),axis = 0)
    
    def normalize(self,low,high,val):
        return ((val - low)/(high-low)-0.5)*2
    
    def fix_overlaps(self):
        # no need to check overlaps
        if len(self.players)<2:
            return
        # Continue to reset players until there are no overlaps
        overlap = True
        while overlap:
            for i in range(len(self.players)):
                for j in range(i+1,len(self.players)):
                    p= [self.players[i].x,self.players[i].y]
                    q= [self.players[j].x,self.players[j].y]
                    if math.dist(p,q)<=2*self.r:
                        self.players[i].reset()
                    elif i == len(self.players)-2 and j == i+1:
                        overlap = False
                        
                        
    def check_collisions(self):
        # Each player checks each platform for collision
        for env_obj in self.env_objects:
            for player in self.players:
                env_collision_gym(player, env_obj)
                env_collision_gym(player, env_obj)
                
        # Each player checks each player for collision
        for i in range(len(self.players)):
            for j in range(i+1,len(self.players)):
                player_collision(self.players[i], self.players[j])
            
        
    
    def reset(self,  seed1 = None, options=None):
        
        # Super.reset function omitted
        # reset players
        for agent in self.players:
            agent.reset()
      
        # Continue to reset players until there are no overlaps
        self.fix_overlaps()
            
        observation = self._get_obs(bad_agent=False)
        

        if self.render_mode == "human":
            self._render_frame()
            
        #info = self._get_info() not used or returned here
        return observation
    
    def make_action(self,agent,action):
        x = int(action)
        d = self._action_to_direction[x]
        
        # Update agent velocity
        agent.move_right(d[0]*self.force)
        agent.move_down(d[1]*self.force)
        if d[2]:
            agent.make_heavy()
    
    
    def step(self, action1):
        
        # if bad agent exists, bad agent acts based off of last obs
        if self.bad_agent_exists:
            action2, _states = self.bad_agent.predict(self._get_obs(bad_agent=True))
            self.make_action(agent = self.p2,action = action2)
        
        
        # Agent 1 acts no matter what
        self.make_action(agent=self.p1,action = action1)
       
        
        self.check_collisions()
        
        # Update players, needs to be fixed
        
        self.p1.update()
        self.p2.update()
       
        # An episode is done if agent or enemy dies
        terminated =  not(self.p1.alive and self.p2.alive)
        reward = -0.001
        if terminated:
            if self.p1.alive:
                reward = 1
            else:
                reward = -1 # Binary sparse rewards
            
        observation = self._get_obs(bad_agent = False)

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
        
        
        # Render agents
        for agent in self.players:
            agent.render(canvas)
        
        # render environment objects
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
