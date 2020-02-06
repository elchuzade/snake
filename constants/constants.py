import pygame

MODE = ["player", "ai"]  # Can also be ai
SPEED = [1, 2, 3, 5, 6, 10, 15, 30]  # Possible speed choices
MARGIN = 20
FPS = 30
GAME_BACKGROUND = (0, 0, 0)  # RGB representation of black screen for pygame
LINE_COLOR = (100, 100, 100)

SCREEN_SIZES = [10, 20, 30]  # Possible choices for a square screen side cells
ACTIONS = [0, 1, 2, 3]  # 0 - go left, 1 - go up, 2 - go right, 3 - go down
MIN_SNAKE_SIZE = 3  # How many cells the snake will hold at the beginning of every game
GRID_LINE_WIDTH = 1
CELL_SIZE = 20
FOOD_SIZE = 16
FOOD_COLOR = (200, 150, 100)
SNAKE_BODY_COLOR = (100, 150, 200)
SNAKE_HEAD_COLOR = (100, 200, 150)
FOOD_CELL_MARGIN = (CELL_SIZE - FOOD_SIZE) / 2
