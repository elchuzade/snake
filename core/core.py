from constants import constants
from helpers import helpers
import random


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

    def get_length(self):
        length = 0
        child = self.head
        while child is not None:
            child = child.child
            length += 1
        return length

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
    def __init__(self, screen_size=constants.SCREEN_SIZES[0]):
        self.food = None
        self.snake = None
        self.direction = 2
        self.screen_size = screen_size
        self.state = self.get_state()  # Make empty state
        self.snake = MySnake()
        self.state = self.get_state()  # Add snake to state
        self.make_food()  # Add food to state
        self.snake_length = self.snake.get_length()

    def reset(self):
        self.food = None
        self.snake = None
        self.direction = 2
        self.state = self.get_state()  # Make empty state
        self.snake = MySnake()
        self.state = self.get_state()  # Add snake to state
        self.make_food()  # Add food to state

    def make_food(self):
        food_x, food_y = self.pick_food_coords()
        if self.food:
            self.food.reinitialize(food_x, food_y)
        else:
            self.food = Food(food_x, food_y)
        self.state = self.get_state()    # Add food to state

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
        random_index = random.randrange(len(empty_index))
        food_x = empty_index[random_index] % (self.screen_size + 2)
        food_y = empty_index[random_index] // (self.screen_size + 2)
        return food_x, food_y

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

        # Check if after this play you have eaten food
        food = self.check_if_food()
        if food:
            self.snake.add_footprint()
            self.state = self.get_state()  # Update state before adding new food
            self.make_food()

        # Check if after this step you have lost
        if self.check_if_lost():
            result = "lost"
            print(result)

        # Check if after this step you have won
        if self.check_if_won():
            result = "win"
            print(result)

        self.snake.remove_tail()

        self.state = self.get_state()
        return self.state
