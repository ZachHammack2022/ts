import bonk_game
import gym
from stable_baselines3 import PPO,A2C,DQN
from sb3_contrib import ARS
from stable_baselines3.common.env_util import make_vec_env
import os

def train(models):
    """Take in predefined models (on specific envs) to train and save the agents

    Args:
        models (dict): (str)Name: (model object) Model
    """
    
    for key in models:
        model = models[key]
        model.learn(total_timesteps=250000,progress_bar=True)
        filename = f"./agents/{key}"
        model.save(filename)

def create_models(env,verbose):
    ars = ARS("LinearPolicy", env, verbose=verbose)
    ppo = PPO("MlpPolicy", env, verbose=verbose)
    a2c = A2C("MlpPolicy", env, verbose=verbose)
    dqn = DQN("MlpPolicy", env, verbose=verbose)
    models = {
        "ppo": ppo,
        "a2c": a2c,
        "dqn": dqn,
        "ars": ars,
    }
    
    
    return models

def delete(models):
    for key in models:
        if (os.path.exists(f"./agents/{key}")):
            os.remove(f"./agents/{key}")
    
        
# Create parallel environments
env = make_vec_env("bonk_game/bonk-v0", n_envs=4)

# Create models
models = create_models(env,verbose = 0)

# Delete old agents from files
delete(models)

# Train agents
train(models)

print("All agents have been trained!")




