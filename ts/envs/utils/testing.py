import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from ts.envs.training_env import TsEnv
import gym
from stable_baselines3 import PPO,A2C,DQN
from sb3_contrib import ARS
import numpy as np

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

#template: model2 = PPO.load("c.zip")
def create_env(render_mode):
    
    env = TsEnv(render_mode)
        
    return env

def run_test(model,env,steps):
        
    obs = env.reset()
    for i in range(steps):
        action, _states = model.predict(obs)
        obs,reward, done, info = env.step(action)
        if done:
            break
    env.close()    
        
def make_statement(agents):
    
    # Prepare statement
    names = list(agents.keys())
    statement = "Your choices for the agent:\n"
    for i,name in enumerate(names):
        statement += f"{i}: {name}\n"
    statement += "Please enter the integer for your selected algorithm: "
    return statement

def create_list(r1, r2):
    return [item for item in range(r1, r2+1)]

def pick_agent(agents):
    pick = -1
    options = set(create_list(0,len(agents)))
    
    while pick not in options:
        statement = make_statement(agents)
        pick = int(input(statement))
    print("-----------------")
    return pick

def get_steps():
    while True:
        steps = int(input("Enter an integer for how many steps (30 per second) you would like to simulate: "))
        if steps>= 0:
            return steps

def test():
    
    models = ({
        "ppo": PPO,
        "a2c": A2C,
        "dqn": DQN,
        "ars": ARS,
    })
    
    inputs = ({
        0: "ppo",
        1: "a2c",
        2: "dqn",
        3: "ars",
    })
    
    
    # load agents
    agents = load_agents(models)
    
    # get a number form the user
    input1 = pick_agent(agents)

    
    # get model string name from dict
    pick1 = inputs[input1]
    
    
    # get model from string name
    agent1 = agents[pick1]


    steps = get_steps()
    
    # Create test environment
    env = create_env(render_mode="human")
        
    
    run_test(agent1,env,steps = steps)