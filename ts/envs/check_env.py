import ts
import gym
from stable_baselines3.common.env_checker import check_env

# Parallel environments
env = gym.make('ts/ts-v0')
check_env(env)