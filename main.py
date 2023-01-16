import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from bonk_game.envs.utils.start import run_game
if __name__ == "__main__":
    run_game()