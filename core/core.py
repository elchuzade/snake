from constants import constants

class SnakeNode:
    def __init__(self, x, y, head):
        self.x = x
        self.y = y
        self.child = head


class Snake:
    def __init__(self):
        self.head = None
        self.size = size_iterator = constants.MIN_SNAKE_SIZE
        head_x = 0
        head_y = 0
        while size_iterator > 0:
            self.head = SnakeNode(head_x, head_y, self.head)
            head_x += 1
            size_iterator -= 1

    def print_snake(self):
        child = self.head
        while child is not None:
            print("x:", child.x, "|", "y:", child.y)
            child = child.child
