This is a working version of bonk.io, a popular online physics-based platform game. This was created using pygame, mostly from scratch aside from the collision functions. This environment supports single agent RL using OpenAI gym and Stable Baselines 3(SB3). 

Currently, only one bonk.io env exists, but multiple envs could easily be created. There are options for multiplayer, AI agent vs user, and AI vs AI (same or different models). Next feature to be implemented is a tourney system where different agents can fight one another. 

Training is done in the training.py file. You can load your agent into the testing.py file to play against itself, other agents, or you. 