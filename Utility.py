from collections import Counter
import copy

class BoardOut:
    def __init__(self):
        self.count = 0
        self.val = 0
        self.list = []

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
        0: is_a_mill(l, t, 2, 4),
        1: is_a_mill(l, t, 3, 5) or is_a_mill(l, t, 8, 17),
        2: is_a_mill(l, t, 0, 4),
        3: is_a_mill(l, t, 1, 5) or is_a_mill(l, t, 7, 14),
        4: is_a_mill(l, t, 0, 2),
        5: is_a_mill(l, t, 1, 3) or is_a_mill(l, t, 6, 11),
        6: is_a_mill(l, t, 5, 11) or is_a_mill(l, t, 7, 8),
        7: is_a_mill(l, t, 6, 8) or is_a_mill(l, t, 3, 14),
        8: is_a_mill(l, t, 6, 7) or is_a_mill(l, t, 1, 17),
        9: is_a_mill(l, t, 10, 11) or is_a_mill(l, t, 12, 15),
        10: is_a_mill(l, t, 9, 11) or is_a_mill(l, t, 13, 16),
        11: is_a_mill(l, t, 9, 10) or is_a_mill(l, t, 14, 17) or is_a_mill(l, t, 5, 6),
        12: is_a_mill(l, t, 13, 14) or is_a_mill(l, t, 9, 15),
        13: is_a_mill(l, t, 12, 14) or is_a_mill(l, t, 10, 16),
        14: is_a_mill(l, t, 12, 13) or is_a_mill(l, t, 11, 17) or is_a_mill(l, t, 3, 7),
        15: is_a_mill(l, t, 16, 17) or is_a_mill(l, t, 9, 12),
        16: is_a_mill(l, t, 15, 17) or is_a_mill(l, t, 10, 13),
        17: is_a_mill(l, t, 15, 16) or is_a_mill(l, t, 11, 14) or is_a_mill(l, t, 1, 8),
    }
    return switcher.get(i, False)

# input : list: board, str: t, int: index1, int: index2
def is_a_mill(board, piece_type, index1, index2, reset_mill_check=False):
    return board[index1] == piece_type and board[index2] == piece_type

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
# Question 1 - 
# Part1:  
# MinMaxOpening.py
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
# Question 1 - 
# Part2: 
# MinMaxGame.py
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

############################################################################################################
# Question 2 - 
# Part1:
# ABOpening.py
############################################################################################################

############################################################################################################
# Question 2 - 
# Part2:
# ABGame.py
############################################################################################################



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
