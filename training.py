import bonk_game
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env
from datetime import datetime

# class Training():
    
#     # Should try to make fps modular
#     def __init__(self,env,models):

# Parallel environments
env = make_vec_env('bonk_game/bonk-v0',n_envs=4)
# check_env(env)
models = {
    "ppo": PPO('MlpPolicy', env, verbose=0,tensorboard_log="./ppo_bonk_tensorboard/")
    }

for key in models:
    model = models[key]
    model.learn(total_timesteps=250000,progress_bar=True)
    model.save(key)

