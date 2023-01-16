import bonk_game
import gym
from stable_baselines3 import PPO,A2C,DQN
from sb3_contrib import ARS
from stable_baselines3.common.env_util import make_vec_env
import os
from bonk_game.envs.testing_env import TestEnv
from bonk_game.envs.match_env import MatchEnv
import random



# pass in a dict to load models with the correct functions
def load_agents(models):
    loaded_agents = {}
    for key in models:
        path = f"./agents/{key}.zip"
        if (os.path.exists(path)):
            file_name = f"./agents/{key}"
            model = models[key]
            agent = model.load(file_name)
            loaded_agents[key] = agent
    return loaded_agents

def run_tournament(participants,steps = 5000):
    while len(participants) >1:
        winners = {}
        for i in range(len(participants)//2):
            # Choose and remove first agent from participants
            key1 = random.choice(list(participants.keys()))
            a1 = participants.pop(key1)
            
            # Choose and remove second agent from participants
            key2 = random.choice(list(participants.keys()))
            a2 = participants.pop(key2) 
            match = MatchEnv(a1,a2,)
            scores = match.simulate(steps)
            print(f"{key1} vs {key2}")
            print(f"{scores[0]}:{scores[1]}")
            if scores[0] >= scores[1]:
                winners.update({key1:a1}) 
            else:
                winners.update({key2:a2})
        # Winners move onto the next round
        participants = winners.copy()
    return winners
    
    
models = {
    "ppo": PPO,
    "a2c": A2C,
    "dqn": DQN,
    "ars": ARS,
}

# Create parallel environments
env = make_vec_env("bonk_game/bonk-v0", n_envs=4)
agents = load_agents(models)
num_agents = len(agents)
assert num_agents in (2,4,8,16)

participants = agents.copy()
winner = run_tournament(participants,steps = 100000)
alg = winner.keys()
print(f"The winner of the tournament is the {list(alg)[0]} agent!")
         
    
    
    

            
            