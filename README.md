This is a working version of bonk.io, a popular online physics-based platform game. This was created using pygame, mostly from scratch aside from the collision functions. This environment supports single agent RL using OpenAI gym and Stable Baselines 3. 

Currently, only one bonk.io env exists, but multiple envs could easily be created. There are options for multiplayer, AI agent vs user, and AI vs AI (same or different training algorithms). Tournaments are supported for AI agents only. User cannot interact in tournament yet.

To run:
1. Install python 3.9
2. Clone repo (if you're unfamiliar, click the green button above and download the zip. Then click the zip to open the files once you download it.)
3. Open terminal, navigate to the working directory (bonk_game-main), and run "python3.9 -m venv ./venv" to create a virtual environment to install our dependencies.
4. Run "source ./venv/bin/activate"
5. Run "pip install -r requirements.txt"
6. Run "pip install -e ." to make the gym environment
7. Run "python3 main.py". This will train your agents and allow you to begin testing.
8. Once you have trained your agents, you can run a tournament. Run "python3 tournament.py". This will put your trained agents against one another to find the winner! 


