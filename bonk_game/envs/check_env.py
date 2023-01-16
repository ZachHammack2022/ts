import bonk_game
import gym
from stable_baselines3.common.env_checker import check_env

# Parallel environments
env = gym.make('bonk_game/bonk-v0')
check_env(env)