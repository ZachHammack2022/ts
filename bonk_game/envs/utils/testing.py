import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from bonk_game.envs.testing_env import TestEnv
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
def create_env(model1,model2,render_mode):
    
    env = TestEnv(model1,model2,render_mode)
    
    # User input will not work with no display initialized
    if model1 == "user" and model2 == "user":
        assert env.render_mode == "human"
        
    return env
    


def run_test(model1,model2,env,steps):
        
    obs = env.reset()
    for i in range(steps):
        if model1 == "user" and model2 == "user":
            actions = ""
        elif model1 == "user":
            actions, _states = model2.predict(obs[12:])
        elif model2 == "user":
            actions, _states = model1.predict(obs[:12])
        else:
            action1, _states = model1.predict(obs[:12])
            action2, _states = model2.predict(obs[12:])
            actions = [action1,action2]
        obs, done, info = env.step(actions)
        if done:
            break
    env.close()
        
        
def make_statement(agents,num):
    
    keys = ({
        "first": "wasd",
        "second": "the arrowpad"
    })
    
    # Prepare statement
    names = list(agents.keys())
    count = len(names)
    statement = f"Your choices for the {num} agent:\n"
    for i,name in enumerate(names):
        statement += f"{i}: {name}\n"
    statement += f"{count}: user input (controlled with {keys[num]})\n"
    statement += f"Please enter the integer for your selected algorithm: "
    return statement

def create_list(r1, r2):
    return [item for item in range(r1, r2+1)]

def pick_agent(agents,num):
    pick = -1
    options = set(create_list(0,len(agents)))
    
    while pick not in options:
        # pick first agent
        statement = make_statement(agents,num)
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
        "bad": PPO,
        "ppo": PPO,
        "a2c": A2C,
        "dqn": DQN,
        "ars": ARS,
    })
    
    inputs = ({
        0: "bad",
        1: "ppo",
        2: "a2c",
        3: "dqn",
        4: "ars",
        5: "user"
    })
    
    
    # load agents
    agents = load_agents(models)
    
    # get a number form the user
    input1 = pick_agent(agents,"first")
    input2 = pick_agent(agents,"second")
    
    # get model string name from dict
    pick1 = inputs[input1]
    pick2 = inputs[input2]
    
    
    agent1 = "user"
    agent2 = "user"
    # get model from string name
    if pick1 != "user":
        agent1 = agents[pick1]
    if pick2 != "user":
        agent2 = agents[pick2]

    steps = get_steps()
    
    # Create test environment
    env = create_env(agent1,agent2,render_mode="human")
        
    
    run_test(agent1,agent2,env,steps = steps)
    
    
    
    
    
    
    
    
    