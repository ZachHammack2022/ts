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
env = make_vec_env('bonk_game/bonk-v0',n_envs=4)
# check_env(env)

model = PPO('MlpPolicy', env, verbose=1,tensorboard_log="./ppo_bonk_tensorboard/")
# 
model.learn(total_timesteps=500000,progress_bar=True,tb_log_name="first_run",reset_num_timesteps=False,log_interval=50000)
model.learn(total_timesteps=500000,progress_bar=True,tb_log_name="second_run",reset_num_timesteps=False,log_interval=50000)
time = datetime.now().strftime('%Y-%m-%d-%H:%M:%S-%p')
file_name = "ppo_bonk" + time
model.save(file_name)

del model # remove to demonstrate saving and loading

model = PPO.load(file_name)

obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    #env.render()

