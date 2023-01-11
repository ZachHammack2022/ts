import bonk_game
import gymnasium as gym
from gymnasium.wrappers import FlattenObservation
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO


import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

# Parallel environments
env = gym.make('bonk_game/bonk-v0')

model = PPO('MultiInputPolicy', env, verbose=1)
model.learn(total_timesteps=2500)
model.save("ppo_bonk")

del model # remove to demonstrate saving and loading

model = PPO.load("ppo_bonk")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()

