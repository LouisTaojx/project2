from collections import Counter
import copy

############################################################################################################
# utility functions start:
############################################################################################################

def swap_board(board):
    swapped = []
    for t in board:
        if t == 'W':  # Assuming 'W' represents white pieces
            swapped.append('B')  # Assuming 'B' represents black pieces
        elif t == 'B':
            swapped.append('W')
        else:
            swapped.append(t)  # Handles cases where t is neither 'W' nor 'B'
    return swapped

def get_neighbors(i):
    switcher = {
        0: [1, 2, 15],
        1: [0, 3, 8],
        2: [0, 3, 4, 13],
        3: [1, 2, 5, 7],
        4: [2, 5, 9],
        5: [3, 4, 6],
        6: [5, 7, 11],
        7: [3, 6, 8, 14],
        8: [1, 7, 17],
        9: [4, 10, 12],
        10: [9, 11, 13],
        11: [6, 10, 14],
        12: [2, 9, 13, 15],
        13: [10, 12, 14, 16],
        14: [7, 11, 13, 17],
        15: [0, 12, 16],
        16: [13, 15, 17],
        17: [8, 14, 16],
    }
    return switcher.get(i, [])

# input : int: index, list: board
def check_for_mills(i, l):
    t = l[i]
    switcher = {
        0: l[2] == t and l[4] == t,
        1: (l[3] == t and l[5] == t) or (l[8] == t and l[17] == t),
        2: l[0] == t and l[4] == t,
        3: (l[1] == t and l[5] == t) or (l[7] == t and l[14] == t),
        4: l[0] == t and l[2] == t,
        5: (l[1] == t and l[3] == t) or (l[6] == t and l[11] == t),
        6: (l[5] == t and l[11] == t) or (l[7] == t and l[8] == t),
        7: (l[6] == t and l[8] == t) or (l[3] == t and l[14] == t),
        8: (l[6] == t and l[7] == t) or (l[1] == t and l[17] == t),
        9: (l[10] == t and l[11] == t) or (l[12] == t and l[15] == t),
        10: (l[9] == t and l[11] == t) or (l[13] == t and l[16] == t),
        11: (l[9] == t and l[10] == t) or (l[14] == t and l[17] == t) or (l[5] == t and l[6] == t),
        12: (l[13] == t and l[14] == t) or (l[9] == t and l[15] == t),
        13: (l[12] == t and l[14] == t) or (l[10] == t and l[16] == t),
        14: (l[12] == t and l[13] == t) or (l[11] == t and l[17] == t) or (l[3] == t and l[7] == t),
        15: (l[16] == t and l[17] == t) or (l[9] == t and l[12] == t),
        16: (l[15] == t and l[17] == t) or (l[10] == t and l[13] == t),
        17: (l[15] == t and l[16] == t) or (l[11] == t and l[14] == t) or (l[1] == t and l[8] == t),
    }
    return switcher.get(i, False)

def generate_add(board):
    l1 = []
    for i, p in enumerate(board):
        if p == 'x':
            dup = board.copy()
            dup[i] = 'W'
            if check_for_mills(i, dup): # int, list
                l1 = generate_remove(dup, l1)
            else:
                l1.append(dup)
    return l1

def generate_remove(board, l):
    count = 0
    for i, p in enumerate(board):
        if p == 'B':
            if not check_for_mills(i, board):
                dup = board.copy()
                dup[i] = 'x'
                l.append(dup)
                count += 1
    if count == 0:
        l.append(board)
    return l

# input: list: board
# output: list: list of possible moves
def generate_hopping(board):
    list1 = []
    for i, p in enumerate(board):
        if p == 'W':
            for j, q in enumerate(board):
                if q == 'x':
                    dup = board.copy()
                    dup[i] = 'x'
                    dup[j] = 'W'
                    if check_for_mills(j, dup):
                        generate_remove(dup, list1)
                    else:
                        list1.append(dup)
    return list1

def generate_move(board):
    list1 = []
    for i, p in enumerate(board):
        if p == 'W':
            neighbors = get_neighbors(i)
            for j in neighbors:
                tmp = board[j]
                if tmp == 'x':
                    dup = board.copy()
                    dup[i] = 'x'
                    dup[j] = 'W'
                    if check_for_mills(j, dup):
                        generate_remove(dup, list1)
                    else:
                        list1.append(dup)
    return list1

############################################################################################################
# Called by [ MinMaxOpening.py, ABOpening.py,
############################################################################################################

# input board is a list of Position(['x', 'W', 'B'])
def static_estimation_for_opening(board):
    c = Counter(board)
    return c['W'] - c['B']

# call by MinMaxOpening.py
# input a list of Position
def generate_moves_opening_for_black(board):
    temp_board =swap_board(board)
    b_moves = generate_add(temp_board)
    for i, move in enumerate(b_moves):
        b_moves[i] = swap_board(move)
    return b_moves

############################################################################################################
# Called by [ MinMaxGame.py, ABGame.py, 
############################################################################################################

def static_estimation_midgame_endgame(board):
    c= Counter(board)
    white_num = c['W']
    black_num = c['B']
    l1 = generate_moves_midgame_endgame_for_black(board)
    num_black_moves = len(l1)
    if black_num <= 2:
        return 10000
    elif white_num <= 2:
        return -10000
    elif num_black_moves == 0:
        return 10000
    else:
        return 1000 * (white_num - black_num) - num_black_moves

def generate_moves_midgame_endgame(board):
    piece = board.count('W')
    if piece == 3:
        return generate_hopping(board)
    else:
        return generate_move(board)

def generate_moves_midgame_endgame_for_black(board):
    temp_board = swap_board(board)
    b_moves = generate_moves_midgame_endgame(temp_board)
    for i, move in enumerate(b_moves):
        b_moves[i] = swap_board(move)
    return b_moves


# def static_estimation_opening_improved(board):
#     return board.get_piece_count('W') + possible_mill_count(board, 'W') - board.get_piece_count('B')

# def static_estimation_midgame_endgame_improved(board):
#     white_num = board.get_piece_count('W')
#     black_num = board.get_piece_count('B')
#     list_ = generate_moves_midgame_endgame_for_black(board)
#     num_black_moves = len(list_)
#     possible_mill_count_ = possible_mill_count(board, 'W')
#     if black_num <= 2:
#         return 10000
#     elif white_num <= 2:
#         return -10000
#     elif num_black_moves == 0:
#         return 10000
#     else:
#         return 1000 * (white_num + possible_mill_count_ - black_num) - num_black_moves


# def possible_mill_count(board, t):
#     count = 0
#     for i, p in enumerate(board.pos_list):
#         if p == t:
#             global check_possible_mill
#             check_possible_mill = True
#             if check_for_mills(board, p, i):
#                 count += 1
#     return count
