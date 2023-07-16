from gym.envs.registration import register

register(
     id="ts/ts-v0",
     entry_point="ts.envs:TsEnv",
     max_episode_steps=15000,
)