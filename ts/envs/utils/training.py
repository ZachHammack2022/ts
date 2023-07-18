import ts
import gym
from stable_baselines3 import PPO,A2C,DQN
from sb3_contrib import ARS
from stable_baselines3.common.env_util import make_vec_env
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


# def train_bad_agent(model):
#     print(f"Training the bad agent.")
#     model.learn(total_timesteps=50000,progress_bar=True)
#     filename = f"./agents/bad"
#     model.save(filename)

def train(models):
    """Take in predefined models (on specific envs) to train and save the agents

    Args:
        models (dict): (str)Name: (model object) Model
    """
    
    # train_bad_agent(models["bad"])
    
    for key in models:
        if key == "bad":
            continue
        model = models[key]
        print(f"Training the {key} agent.")
        model.learn(total_timesteps=500000,progress_bar=True)
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

def delete_models(models):
    for key in models:
        if (os.path.exists(f"./agents/{key}")):
            os.remove(f"./agents/{key}")

def check_agents():
    models = models = ({
        "ppo": PPO,
        "a2c": A2C,
        "dqn": DQN,
        "ars": ARS,
    })
    agents = False
    for key in models:
        path = f"./agents/{key}.zip"
        if (os.path.exists(path)):
            agents = True
    return agents
            
    

def train_models():
    # Create parallel environments
    env = make_vec_env("ts/ts-v0", n_envs=4)

    # Create models
    models = create_models(env,verbose = 0)

    # Delete old agents from files
    delete_models(models)

    # Train agents
    train(models)

    print("All agents have been trained!")



