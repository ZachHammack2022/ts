""" This file contains the main game loop."""
import  pygame
import gym
from gym import spaces
import random
import numpy as np
from stable_baselines3 import PPO
from bonk_game.envs.player import *
from bonk_game.envs.platform import *
from bonk_game.envs.mechanics import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    QUIT,
)

def keydown(key,player):
    
    if key == K_UP:
        player.y_v -=1
    elif key == K_DOWN:
        player.y_v +=1
    elif key == K_LEFT:
        player.x_v -=1
    elif key == K_RIGHT:
        player.x_v +=1
    elif key == K_SPACE:
        player.heavy = True
        
def keyup(event,player):
     if event.key == K_SPACE:
        player.heavy = False
def draw(surface,objects,score):
    # draw surface onto backgrond
    # surface.blit(img,(25, 25))
    for object in objects:
        object.render(surface)
     #update scores
    if score:
        myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
        label1 = myfont1.render("Score "+str(objects[1].opp_score), 1, (0,0,0))
        surface.blit(label1, (50,20))

        myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
        label2 = myfont2.render("Score "+str(objects[0].opp_score), 1, (0,0,0))
        surface.blit(label2, (470, 20))  
        
def normalize(low,high,val):
        return ((val - low)/(high-low)-0.5)*2
    
def handle_action(action,agent):
    action_to_direction = {
            0: np.array([1, 0]),
            1: np.array([0, 1]),
            2: np.array([-1, 0]),
            3: np.array([0, -1]),
            4: np.array([1, 1]),
            5: np.array([1, -1]),
            6: np.array([-1, 1]),
            7: np.array([-1, -1])
        }
    x = int(action)
    direction = action_to_direction[x]
    agent.x_v += direction[0]
    agent.y_v += direction[1]
    
    
        


def game_loop(render):
    
    # import pygame module
    pygame.init()
    fps = pygame.time.Clock()
    
    # width,height, bg color
    width,height = 680,480
    dims = [width,height]
    bg_color = (255, 255, 255)
    screen = pygame.display
    screen.set_caption('Bonk.io Simulation')
    surface = screen.set_mode(dims)
    ai_agent = PPO.load("ppo_agent.zip")
    
    # # set the image which to be displayed on screen
    # img = pygame.image.load('assets/white_background.jpeg')
     # dimensions to start players between
    left = 100
    right = 580
    top = 135
    bottom = 420
    
    start_width = (right-left-21)
    start_height = (bottom-top-21)
    
    # Initialize players
    x1,y1  = left+ 21+ np.random.random()*start_width,top+ 21+ np.random.random()*start_height
    p1_color = (255,102,102)
    p2_color = (0,102,204)
    x2,y2 = left+ 21+ np.random.random()*start_width,top+ 21+ np.random.random()*start_height
    # ensure agents have appropriate distance between them
    while abs(x1-x2)<25:
        x2,y2 = left+ 21+ np.random.random()*start_width,top+ 21+ np.random.random()*start_height
    
    
    p1 = player(x1,y1,p1_color)
    p2 = player(x2,y2,p2_color)
    players = [p1,p2]
    
    
    
    # Initialize platforms
    ceiling_color = (255,204,204)
    wall_color = (32,32,32)
    floor = platform(left,right,bottom,bottom+15,ceiling_color,kill = False)
    left_wall = platform(left-20,left,top-20,bottom+15,wall_color,kill = True)
    right_wall = platform(right,right+20,top-20,bottom+15,wall_color,kill = True)
    ceiling = platform(left,right,top-20,top,ceiling_color,kill = False)
    env_objects = [floor,left_wall,right_wall,ceiling]
    ## Key down Events
    #keydown handler
    # set window  (need to define event handlers for each input)
    window = True
    while window:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == K_ESCAPE:
                window = False
        
        # move player_controlled agent
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            keydown(K_LEFT,p1)
        if keys[pygame.K_RIGHT]:
            keydown(K_RIGHT,p1)
        if keys[pygame.K_UP]:
            keydown(K_UP,p1)
        if keys[pygame.K_DOWN]:
            keydown(K_DOWN,p1)
        
        # move AI agent
        ## update observations before passing
        obs = np.zeros(10)
        obs[0] = normalize(left,right,p2.x)
        obs[1] = normalize(bottom,top,p2.y)
        obs[2] = normalize(-15,15,p2.x_v)
        obs[3] = normalize(-15,15,p2.y_v)
        obs[4] = 1.0
        
        obs[5] = normalize(left,right,p1.x)
        obs[6] = normalize(bottom,top,p1.y)
        obs[7] = normalize(-15,15,p1.x_v)
        obs[8] = normalize(-15,15,p1.y_v)
        obs[9] = 1.0
        action, _states = ai_agent.predict(obs)
        handle_action(action,p2)
        
                
        # fill background
        surface.fill(bg_color)
      
    # update players
        for env_obj in env_objects:
            env_collision_game(p1, env_obj)
            env_collision_game(p2, env_obj)
        player_collision(p1, p2)
        p1.update(p2.opp_score)
        p2.update(p1.opp_score)

        
        if not (p1.alive and p2.alive) or (p1.score+p2.score ==100):
            window = False
                
        # draw
        draw(surface,env_objects,False)
        draw(surface,players,True)
        # copy surface to screen
        screen.update()
        fps.tick(60)
    pygame.quit()
  