from constants import constants
from helpers import helpers
import random
import pygame
import numpy as np

class Model:
    def __init__(self):
        self.placeholder = True

    def predict(self, state):
        action = random.randrange(4)
        return action


class SnakeNode:
    def __init__(self, x, y, head=None):
        self.x = x
        self.y = y
        self.child = head


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def reinitialize(self, x, y):
        self.x = x
        self.y = y


class MySnake:
    def __init__(self):
        self.head = None
        self.size = size_iterator = constants.MIN_SNAKE_SIZE
        head_x = 1
        head_y = 1
        self.footprint = SnakeNode(head_x, head_y)
        while size_iterator > 0:
            self.head = SnakeNode(head_x, head_y, self.head)
            head_x += 1
            size_iterator -= 1

    def reinitialize(self):
        self.head = None
        self.size = size_iterator = constants.MIN_SNAKE_SIZE
        head_x = 1
        head_y = 1
        self.footprint = SnakeNode(head_x, head_y)
        while size_iterator > 0:
            self.head = SnakeNode(head_x, head_y, self.head)
            head_x += 1
            size_iterator -= 1

    def get_size(self):
        child = self.head
        count = 0
        while child is not None:
            child = child.child
            count += 1
        return count

    def print_snake(self):
        child = self.head
        while child is not None:
            print("x:", child.x, "|", "y:", child.y)
            child = child.child

    def add_footprint(self):
        child = self.head
        while child.child is not None:
            child = child.child
        child.child = self.footprint

    def remove_tail(self):
        child = self.head
        while child.child.child is not None:
            child = child.child

        self.footprint = child.child
        child.child = None

    def move(self, direction):
        # Create a head at a new position of snake's head depending on where it moves
        if direction == 0:  # Move Left
            new_head = SnakeNode(self.head.x - 1, self.head.y, self.head)
        elif direction == 1:  # Move Up
            new_head = SnakeNode(self.head.x, self.head.y - 1, self.head)
        elif direction == 2:  # Move Right
            new_head = SnakeNode(self.head.x + 1, self.head.y, self.head)
        else:  # Move Down
            new_head = SnakeNode(self.head.x, self.head.y + 1, self.head)

        # Append that new head to the beginning of a snake
        self.head = new_head


class Snake:
    """Snake game environment"""
    def __init__(self, mode=constants.GAME_MODE, screen_size=constants.SCREEN_SIZES[0], speed=constants.GAME_SPEED):
        self.mode = mode
        self.action_frequency = constants.FPS / speed
        self.action_taken = False  # To restrict input actions with game step actions
        self.action_size = len(constants.ACTIONS)  # Output of NN
        self.state_size = int((screen_size + 2) * (screen_size + 2))  # Input to NN
        self.food = None
        self.snake = None
        self.direction = 2
        self.screen_size = screen_size
        self.state = self.get_state()  # Make empty state
        self.snake = MySnake()
        self.state = self.get_state()  # Add snake to state
        self.make_food()  # Add food to state
        self.snake_size = self.snake.get_size()
        self.model = Model()

    def reset(self):
        self.food = None
        self.snake = None
        self.direction = 2
        self.state = self.get_state()  # Make empty state
        self.snake = MySnake()
        self.state = self.get_state()  # Add snake to state
        self.make_food()  # Add food to state

    def __initialize_game(self):
        pygame.init()
        pygame.display.set_caption("Snake Game by {}".format(self.mode))
        size = (self.screen_size + 2) * constants.CELL_SIZE, (self.screen_size + 2) * constants.CELL_SIZE
        screen = pygame.display.set_mode(size)
        # Clock is set to keep track of frames
        clock = pygame.time.Clock()
        pygame.display.flip()
        frame = 1
        while True:
            clock.tick(constants.FPS)
            pygame.event.pump()
            for event in pygame.event.get():
                # Quit the game if the X symbol is clicked
                if event.type == pygame.QUIT:
                    print("pressing escape")
                    pygame.quit()
                    raise SystemExit

                if self.mode == "player" and not self.action_taken:
                    # Look for any button press action
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            action = 0  # 0 means go left
                            self.step(action)

                        elif event.key == pygame.K_UP:
                            action = 1  # 1 means go up
                            self.step(action)

                        elif event.key == pygame.K_RIGHT:
                            action = 2  # 2 means go right
                            self.step(action)

                        elif event.key == pygame.K_DOWN:
                            action = 3  # 3 means go down
                            self.step(action)

            if self.mode == "ai":
                if frame % self.action_frequency == 0:
                    reshaped_state = np.reshape(self.state, [1, self.state_size])
                    action = self.model.predict(reshaped_state)
                    _ = self.step(action)
                    if self.check_if_lost() or self.check_if_lost():
                        self.reset()

            # Build up a black screen as a game background
            screen.fill(constants.GAME_BACKGROUND)

            helpers.draw_state(screen, self.screen_size, self.snake, self.food)

            # if frame % self.action_frequency == 0:
            #     self.action_taken = False

            # Update display
            pygame.display.flip()
            frame += 1

    def play(self):
        self.__initialize_game()

    def make_food(self):
        food_x, food_y = self.pick_food_coords()
        if food_x and food_y:
            if self.food:
                self.food.reinitialize(food_x, food_y)
            else:
                self.food = Food(food_x, food_y)

        self.state = self.get_state()    # Add food to state if food coordinates exist

    def print_snake(self):
        self.snake.print_snake()

    def snake_size(self):
        self.snake.get_size()

    def check_if_lost(self):
        child = self.snake.head.child
        # Head is on top of a body cell "hit itself"
        while child.child is not None:
            if child.x == self.snake.head.x and child.y == self.snake.head.y:
                return True
            child = child.child

        # Head is outside of game boundaries "hit a wall"
        if self.snake.head.x == 0 or self.snake.head.x == len(self.state) - 1 \
                or self.snake.head.y == 0 or self.snake.head.y == len(self.state) - 1:
            return True

        return False

    def check_if_won(self):
        if self.snake_size == self.screen_size * self.screen_size:
            print("You won!")
            return True

        return False

    def check_if_food(self):
        if self.snake.head.x == self.food.x and self.snake.head.y == self.food.y:
            return True
        return False

    def get_state(self):
        return helpers.make_state(self.screen_size, self.snake, self.food)

    def print_state(self):
        for row in self.state:
            print(row)

    def pick_food_coords(self):
        empty_state, empty_index = helpers.empty_cells(self.state)
        if len(empty_index) > 0:
            random_index = random.randrange(len(empty_index))
            food_x = empty_index[random_index] % (self.screen_size + 2)
            food_y = empty_index[random_index] // (self.screen_size + 2)
            return food_x, food_y
        else:
            return None, None

    def step(self, given_direction):
        # If a given is opposite to current direction -> move in a current direction else in a given direction
        # Possible directions 0, 1, 2, 3. Absolute of difference between opposite directions is always 2
        difference = self.direction - given_direction
        if abs(difference) == 2:
            # Given direction is opposite to the current direction of a snake, move in a current direction
            self.snake.move(self.direction)
        else:
            self.snake.move(given_direction)
            self.direction = given_direction

        self.snake.remove_tail()

        # Check if after this play you have eaten food
        if self.check_if_food():
            self.snake.add_footprint()
            self.state = self.get_state()  # Update state before adding new food
            self.snake_size += 1
            if not self.check_if_won():
                self.make_food()

        # Check if after this step you have lost
        if self.check_if_lost():
            result = "lost"

        # Check if after this step you have won
        if self.check_if_won():
            result = "win"
            print(result)

        self.state = self.get_state()
        return self.state
