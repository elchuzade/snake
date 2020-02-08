"""

-1   -1   -1   -1   -1   -1   -1   -1

-1    1    1    2    0    0    0   -1

-1    0    0    0    0    0    0   -1

-1    0    0    0    0    0    0   -1

-1    0    0    0    3    0    0   -1

-1    0    0    0    0    0    0   -1

-1    0    0    0    0    0    0   -1

-1   -1   -1   -1   -1   -1   -1   -1

"""
import pygame
from constants import constants


def make_zeros(screen_size):
    # Build up a matrix of zeros to represent a state
    matrix = []
    for row in range(screen_size):
        row = []
        for col in range(screen_size):
            row.append(0)
        matrix.append(row)

    return matrix


def add_state_margin(matrix):
    # Cover the matrix of zeros that represent a state with -1 values around
    matrix_with_margin = []
    first_row = []
    for i in range(len(matrix) + 2):
        first_row.append(-1)

    last_row = first_row
    matrix_with_margin.append(first_row)

    for row in matrix:
        middle_row = [-1]
        middle_row.extend(row)
        middle_row.append(-1)
        matrix_with_margin.append(middle_row)

    matrix_with_margin.append(last_row)

    return matrix_with_margin


def add_snake(matrix, snake):
    # Add head of a snake
    matrix[snake.head.y][snake.head.x] = 2
    # Add body of a snake
    child = snake.head
    while child.child is not None:
        matrix[child.child.y][child.child.x] = 1
        child = child.child

    return matrix


def add_food(matrix_snake, food):
    matrix_snake[food.y][food.x] = 3
    return matrix_snake


def make_state(screen_size, snake=None, food=None):
    matrix = make_zeros(screen_size)
    matrix_margin = add_state_margin(matrix)

    matrix_snake = matrix_margin

    if snake:
        matrix_snake = add_snake(matrix_margin, snake)

    matrix_food = matrix_snake

    if food:
        matrix_food = add_food(matrix_snake, food)

    return matrix_food


def flatten_index_state(state):
    flat_state = []
    flat_index = []
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            flat_index.append(i * len(row) + j)
            flat_state.append(col)

    return flat_state, flat_index


def remove_margin_coords(flat_state, flat_index):
    removed_flat_state = []
    removed_flat_index = []
    for i in range(len(flat_state)):
        if flat_state[i] != -1:
            removed_flat_state.append(flat_state[i])
            removed_flat_index.append(flat_index[i])

    return removed_flat_state, removed_flat_index


def remove_snake_coords(flat_state_margin, flat_index_margin):
    removed_flat_state = []
    removed_flat_index = []
    for i in range(len(flat_state_margin)):
        # Remove snake and food
        if flat_state_margin[i] != 1 and flat_state_margin[i] != 2 and flat_state_margin[i] != 3:
            removed_flat_state.append(flat_state_margin[i])
            removed_flat_index.append(flat_index_margin[i])

    return removed_flat_state, removed_flat_index


def empty_cells(state):
    flat_state_margin, flat_state_index = flatten_index_state(state)
    flat_state_margin, flat_index_margin = remove_margin_coords(flat_state_margin, flat_state_index)
    flat_state_snake, flat_index_snake = remove_snake_coords(flat_state_margin, flat_index_margin)
    return flat_state_snake, flat_index_snake


"""PYGAME DRAWING FUNCTIONS"""


def draw_grid(screen, size):
    # Draws a grid to separate each game cell
    for i in range(size + 1):
        pygame.draw.rect(screen, constants.LINE_COLOR,
                         (i * constants.CELL_SIZE + constants.CELL_SIZE - constants.GRID_LINE_WIDTH / 2, 0,
                          constants.GRID_LINE_WIDTH, constants.CELL_SIZE * (size + 2)))
    for i in range(size + 1):
        pygame.draw.rect(screen, constants.LINE_COLOR,
                         (0, i * constants.CELL_SIZE + constants.CELL_SIZE - constants.GRID_LINE_WIDTH / 2,
                          constants.CELL_SIZE * (size + 2), constants.GRID_LINE_WIDTH))


def draw_food(screen, food):
    # Draws a circle based on foods x and y coordinates
    pygame.draw.circle(screen, constants.FOOD_COLOR,
                       [int(food.x * constants.CELL_SIZE + constants.CELL_SIZE / 2),
                        int(food.y * constants.CELL_SIZE + constants.CELL_SIZE / 2)],
                       int(constants.FOOD_SIZE / 2))


def draw_snake_head(screen, head):
    pygame.draw.rect(screen, constants.SNAKE_HEAD_COLOR, (head.x * constants.CELL_SIZE,
                                                          head.y * constants.CELL_SIZE,
                                                          constants.CELL_SIZE, constants.CELL_SIZE))


def draw_snake_body(screen, body):
    pygame.draw.rect(screen, constants.SNAKE_BODY_COLOR, (body.x * constants.CELL_SIZE,
                                                          body.y * constants.CELL_SIZE,
                                                          constants.CELL_SIZE, constants.CELL_SIZE))


def draw_snake(screen, snake):
    # Draws rectangles on each cell of snake's coordinates
    draw_snake_head(screen, snake.head)
    snake_body = snake.head.child
    while snake_body is not None:
        draw_snake_body(screen, snake_body)
        snake_body = snake_body.child


def draw_margin(screen, size):
    # Left line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, constants.MARGIN,
                                                           constants.MARGIN, constants.CELL_SIZE * size))
    # Right line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND,
                     (constants.MARGIN + constants.CELL_SIZE * size, constants.MARGIN,
                      constants.MARGIN, constants.CELL_SIZE * size))
    # Top line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, 0,
                                                           constants.MARGIN * 2 + constants.CELL_SIZE * size,
                                                           constants.MARGIN))
    # Bottom line margin
    pygame.draw.rect(screen, constants.MARGIN_BACKGROUND, (0, constants.MARGIN + constants.CELL_SIZE * size,
                                                           constants.MARGIN * 2 + constants.CELL_SIZE * size,
                                                           constants.MARGIN))


def draw_state(screen, size, snake, food):
    # Draw everything on the map
    draw_grid(screen, size)
    draw_margin(screen, size)
    draw_snake(screen, snake)
    draw_food(screen, food)
