import bonk_game
import gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env
from datetime import datetime

# Parallel environments
env = make_vec_env('bonk_game/bonk-v0',n_envs=4)
# check_env(env)

model = PPO('MlpPolicy', env, verbose=0,tensorboard_log="./ppo_bonk_tensorboard/")
# 
model.learn(total_timesteps=250000,progress_bar=True,tb_log_name="first_run",reset_num_timesteps=False,log_interval=50000)
time = datetime.now().strftime('_%d-%H:%M%p')
# file_name = "ppo_bonk" + time
file_name = "c"
model.save(file_name)

