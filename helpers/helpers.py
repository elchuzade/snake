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


def make_state(screen_size):
    matrix = make_zeros(screen_size)
    matrix_with_margin = add_state_margin(matrix)
    return matrix_with_margin
