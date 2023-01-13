#from gymnasium.envs.registration import register
from gym.envs.registration import register

register(
     id="bonk_game/bonk-v0",
     entry_point="bonk_game.envs:BonkEnv",
     max_episode_steps=10000,
)