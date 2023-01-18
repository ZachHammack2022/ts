from bonk_game.envs.testing_env import TestEnv
import gym

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env


class MatchEnv():
    
    # Should try to make fps modular
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 20}
    def __init__(self,agent1, agent2, render_mode = None):

        # user participation in tournament currently not supported
        assert agent1 is not None and agent2 is not None
        
        # Create Testing Env
        self.env = TestEnv(agent1,agent2)
        self.agent1 = agent1
        self.agent2 = agent2

    
    def simulate(self,steps):
        obs = self.env.reset()
        for i in range(steps):
            action1, _states = self.agent1.predict(obs[:12])
            action2, _states = self.agent2.predict(obs[12:])
            obs, done, info = self.env.step([action1,action2])
            if done:
                break
        return self.env.scores