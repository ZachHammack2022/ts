import bonk_game
import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

# Just one environment
env = gym.make('bonk_game/bonk-v0',render_mode = "human")
model = PPO.load("b.zip")
obs = env.reset()
for i in range(5000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    if done:
        obs = env.reset()
