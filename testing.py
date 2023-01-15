from bonk_game.envs.testing_env import TestEnv
import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

#template: model2 = PPO.load("c.zip")

# Just one environment
model1 = PPO.load("ppo_agent.zip")
model2 = PPO.load("ppo_agent.zip")
env = TestEnv(model1,model2,render_mode="human")

# User input will not work with no display initialized
if model1 is None and model2 is None:
    assert env.render_mode == "human" or env.render_mode == "rgb_array"
    
obs = env.reset()
for i in range(5000):
    if model1 is None and model2 is None:
        actions = ""
    elif model1 is None:
        actions, _states = model2.predict(obs[10:])
    elif model2 is None:
        actions, _states = model1.predict(obs[:10])
    else:
        action1, _states = model1.predict(obs[:10])
        action2, _states = model2.predict(obs[10:])
        actions = [action1,action2]
    obs, done, info = env.step(actions)
    if done:
        break