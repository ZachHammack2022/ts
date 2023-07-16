
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from ts.envs.utils.control import game_loop
"""Runs control's main game loop."""

def run_game():
    game_loop()