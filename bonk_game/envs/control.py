""" This file contains the main game loop."""
import  pygame
import random
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
    
    # # set the image which to be displayed on screen
    # img = pygame.image.load('assets/white_background.jpeg')
    
    # Initialize players
    p1_color = (255,102,102)
    p2_color = (0,102,204)
    p1 = player(200,200,p1_color)
    p2 = player(400,200,p2_color)
    players = [p1,p2]
    

    
    # Initialize platforms
    ceiling_color = (255,204,204)
    wall_color = (32,32,32)
    floor = platform(100,580,420,435,ceiling_color,kill = False)
    left_wall = platform(80,100,115,435,wall_color,kill = True)
    right_wall = platform(580,600,115,435,wall_color,kill = True)
    ceiling = platform(100,580,115,135,ceiling_color,kill = False)
    env_objects = [floor,left_wall,right_wall,ceiling]
    ## Key down Events
    #keydown handler
    # set window  (need to define event handlers for each input)
    window = True
    while window:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == K_ESCAPE:
                window = False
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            keydown(K_LEFT,p1)
        if keys[pygame.K_RIGHT]:
            keydown(K_RIGHT,p1)
        if keys[pygame.K_UP]:
            keydown(K_UP,p1)
        if keys[pygame.K_DOWN]:
            keydown(K_DOWN,p1)
                
        # fill background
        surface.fill(bg_color)
      
    # update players
        for env_obj in env_objects:
            env_collision(p1, env_obj)
            env_collision(p2, env_obj)
        player_collision(p1, p2)
        p1.update(p2.opp_score)
        p2.update(p1.opp_score)
        print(p1.x_v)
        
        if not (p1.alive and p2.alive) or (p1.score+p2.score ==10):
            window = False
                
        # draw
        draw(surface,env_objects,False)
        draw(surface,players,True)
        # copy surface to screen
        screen.update()
        fps.tick(60)
    pygame.quit()
  