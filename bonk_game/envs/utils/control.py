import bonk_game
import gym
from stable_baselines3 import PPO,A2C,DQN
from sb3_contrib import ARS
from stable_baselines3.common.env_util import make_vec_env
import os
from bonk_game.envs.utils.training import train_models,check_agents
from bonk_game.envs.utils.testing import test



def game_loop():
    # Train various agents to play bonk.io
    already_trained= check_agents()
    if not already_trained:
        print("Training your agents. This should take 100-15 minutes.\n \n")
        train_models()
    else:
        print("Your agents are already trained! We can go straight to testing.\n \n")
    
    test()