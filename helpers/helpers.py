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
    matrix[snake.head.y + 1][snake.head.x + 1] = 2
    # Add body of a snake
    child = snake.head.child
    while child is not None:
        matrix[child.y + 1][child.x + 1] = 1
        child = child.child

    return matrix


def make_state(screen_size, snake, food=None):
    matrix = make_zeros(screen_size)
    matrix_margin = add_state_margin(matrix)
    matrix_snake = add_snake(matrix_margin, snake)

    return matrix_snake


def flatten_index_state(state):
    flat_state = []
    flat_index = []
    for i, row in enumerate(state):
        for j, col in enumerate(row):
            flat_index.append(i*len(row) + j)
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
        if flat_state_margin[i] != 1 and flat_state_margin[i] != 2:
            removed_flat_state.append(flat_state_margin[i])
            removed_flat_index.append(flat_index_margin[i])

    return removed_flat_state, removed_flat_index


def empty_cells(state):
    flat_state_margin, flat_state_index = flatten_index_state(state)
    flat_state_margin, flat_index_margin = remove_margin_coords(flat_state_margin, flat_state_index)
    flat_state_snake, flat_index_snake = remove_snake_coords(flat_state_margin, flat_index_margin)
    return flat_state_snake, flat_index_snake
