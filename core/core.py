from constants import constants

class SnakeNode:
    def __init__(self, x, y, head):
        self.x = x
        self.y = y
        self.child = head


class MySnake:
    def __init__(self):
        self.head = None
        self.size = size_iterator = constants.MIN_SNAKE_SIZE
        head_x = 0
        head_y = 0
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

    def remove_tail(self):
        child = self.head
        while child.child.child is not None:
            child = child.child

        child.child = None

    def move(self, direction):
        print(direction)
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
    def __init__(self):
        self.direction = 2
        self.snake = MySnake()

    def print_snake(self):
        self.snake.print_snake()

    def snake_size(self):
        self.snake.get_size()

    def check_if_lost(self):
        return False

    def check_if_won(self):
        return False

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

        result = "play"
        # Check if after this step you have lost
        if self.check_if_lost():
            result = "lost"
        # Check if after this step you have won
        if self.check_if_won():
            result = "win"

        if result == "play":
            self.snake.remove_tail()
