import numpy as np 
import gym
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
from bonk_game.envs.utils.player import player
from bonk_game.envs.utils.platform import platform
from bonk_game.envs.utils.mechanics import env_collision_game,player_collision
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_CAPSLOCK,
    K_w,
    K_a,
    K_s, 
    K_d,
)

class TestEnv():
    
    # Should try to make fps modular
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}
    def __init__(self,model1, model2, render_mode = None):
        
        self.user1 = False
        self.user2 = False
        self.model1 = None
        self.model2 = None
        # initialize models
        if model1 == "user":
            self.user1 = True
        if model2 == "user":
            self.user2 = True
        
        if not self.user1:
            self.model1 = model1
        if not self.user2:
            self.model2 = model2
        
        # dimensions of screen
        self.width = 680
        self.height = 480 
        # dimensions to start players between
        self.left = 100
        self.right = 580
        self.top = 135
        self.bottom = 420
        self.r = 20
        self.force = 2 # force players experience on input
        
        # Initialize players
        p1_color = (255,102,102)
        p2_color = (0,102,204)
        self.p1 = player(self.r,self.left,self.right,self.top,self.bottom,p1_color)
        self.p2 = player(self.r,self.left,self.right,self.top,self.bottom,p2_color)
        self.players = [self.p1,self.p2]
        self.scores = [self.p1.score,self.p2.score]
        
        # dimensions to start players between
        self.left = 100
        self.right = 580
        self.top = 135
        self.bottom = 420
    
        # Initialize platforms
        ceiling_color = (255,204,204)
        wall_color = (32,32,32)
        
        self.floor = platform(self.left,self.width-self.left,self.bottom,self.bottom+15,ceiling_color,kill = False)
        self.left_wall = platform(self.left-20,self.left,self.top-20,self.bottom+15,wall_color,kill = True)
        self.right_wall = platform(self.right,self.right+20,self.top-20,self.bottom+15,wall_color,kill = True)
        self.ceiling = platform(self.left,self.right,self.top-20,self.top,ceiling_color,kill = False)
        self.env_objects = [self.floor,self.left_wall,self.right_wall,self.ceiling]
        
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
    
    # need to flip for one of the agents
    def _get_obs(self):
        a = np.concatenate((self.p1.get_obs(),self.p2.get_obs()),axis = 0)
        b = np.concatenate((self.p2.get_obs(),self.p1.get_obs()),axis = 0)
        return np.concatenate((a,b),axis = 0)
    
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
                if player == self.p1:
                    self.p2.score += env_collision_game(player, env_obj)
                elif player == self.p2:
                    self.p1.score += env_collision_game(player, env_obj)
                
        # Each player checks each player for collision
        for i in range(len(self.players)):
            for j in range(i+1,len(self.players)):
                player_collision(self.players[i], self.players[j])
                
    def agent_action(self,agent,action):
        # Map the action to change in acceleration
        # not sure why i need to cast this from np int to int
        x = int(action)
        d = self._action_to_direction[x]
        
        # Update agent velocity
        agent.move_right(d[0]*self.force)
        agent.move_down(d[1]*self.force)
        if d[2]:
            agent.make_heavy()
    
    def check_keydown(self,keys,agent):
        if agent == self.p2:
            if keys[pygame.K_LEFT]:
                agent.move_left(self.force)
            if keys[pygame.K_RIGHT]:
                agent.move_right(self.force)
            if keys[pygame.K_UP]:
                agent.move_up(self.force)
            if keys[pygame.K_DOWN]:
                agent.move_down(self.force)
            if keys[pygame.K_SPACE]:
                agent.make_heavy()
        else:
            if keys[pygame.K_w]:
                agent.move_up(self.force)
            if keys[pygame.K_a]:
                agent.move_left(self.force)
            if keys[pygame.K_s]:
                agent.move_down(self.force)
            if keys[pygame.K_d]:
                agent.move_right(self.force)
            if keys[pygame.K_CAPSLOCK]:
                agent.make_heavy()
                
    def apply_forces(self,actions):
        # Update velocity for AI agents and users
        if self.user1 or self.user2:
            keys = pygame.key.get_pressed()
        # If user is player, get action from keys
        if self.user1:
           self.check_keydown(keys,self.p1)
        # if p1 is AI and p2 is user, actions controls p1 action
        elif self.user2:
           self.agent_action(self.p1,actions)
        # both ai, actions[0] control p1
        else:
            self.agent_action(self.p1,actions[0])
        # If user is player, get action from keys
        if self.user2:
            self.check_keydown(keys,self.p2)
        # if p2 is AI and p1 is user, actions controls p2 action
        elif self.user1:
           self.agent_action(self.p2,actions)
        # both ai, actions[1] control p2
        else:
            self.agent_action(self.p2,actions[1])
                
        
    
    def reset(self):
        # reset players
        for agent in self.players:
            agent.reset()
      
        # Continue to reset players until there are no overlaps
        self.fix_overlaps()
            
        obs = self._get_obs()

        if self.render_mode == "human":
            self._render_frame()
            
        return obs
    
    
    def step(self, forces):
        
        self.apply_forces(forces)
        self.check_collisions()
        
        # Update players
        self.p1.update()
        self.p2.update()
        
        # Update scores for rendering
        self.scores = [self.p1.score,self.p2.score]
       
        # An episode is done if agent or enemy dies
        high_score = 100
        terminated =  (self.p1.score == high_score or self.p2.score == high_score)
    
            
        obs = self._get_obs()

        if self.render_mode == "human":
            self._render_frame()
        info = {}
        
        return obs, terminated, info
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        
    def render_score(self,canvas):
        myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
        label1 = myfont1.render("Score "+ str(self.scores[0]), 1, (0,0,0))
        canvas.blit(label1, (50,20))

        myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
        label2 = myfont2.render("Score "+str(self.scores[1]), 1, (0,0,0))
        canvas.blit(label2, (470, 20))
        
    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.width, self.height)
            )
            #self.window.set_caption('Bonk.io Testing')
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
            
        # render scores
        self.render_score(canvas)
    
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
