from gym.envs.registration import register

register(
     id="ts/ts-v0",
     entry_point="ts.envs.training_env:TsEnv",
     max_episode_steps=1000,
)