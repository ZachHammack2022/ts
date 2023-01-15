from bonk_game.envs.testing_env import TestEnv
import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

# Just one environment
model1 = PPO.load("b.zip")
model2 = PPO.load("b.zip")
env = TestEnv(model1,model2,render_mode="human")
obs = env.reset()
for i in range(5000):
    action1, _states = model1.predict(obs[:10])
    action2, _states = model1.predict(obs[10:])
    actions = [action1,action2]
    obs, done, info = env.step(actions)
    if done:
        break