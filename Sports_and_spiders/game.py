import pygame
import random
import json
from Sports_and_spiders.objectSandS import Image, Sound, Box, Text
import traceback
import sys
import os


class Game:
    def __init__(self, grade, lesson):
        pass



def play_S_and_S(grade, lesson):
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        with open("error_log.txt", "a") as f:
            f.write("Mixer init failed:\n")
            f.write(traceback.format_exc())
    try:
        game = Game(grade, lesson)
    except Exception:
        with open("error_log.txt", "a") as f:
            f.write("loading game error:\n")
            f.write(traceback.format_exc())
    game.main_loop()
    pygame.quit()
