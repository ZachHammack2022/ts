import bonk_game
# gymnasium as gym
import gym
# #from gymnasium.wrappers import FlattenObservation
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.vec_env.base_vec_env import VecEnv, VecEnvStepReturn, VecEnvWrapper
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO


# #import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

from datetime import datetime

# Parallel environments
env = gym.make('bonk_game/bonk-v0',render_mode = "human")
model = PPO.load("ppo_agent.zip")
obs = env.reset()
print(obs)
for i in range(5000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        obs = env.reset()
        print(obs)
