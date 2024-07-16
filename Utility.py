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

def generate_remove(board, index):
    count = 0
    for i, p in enumerate(board):
        if p == 'B':
            if not check_for_mills(i, board):
                dup = board.copy()
                dup[i] = 'x'
                index.append(dup)
                count += 1
    if count == 0:
        index.append(board)
    return index

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

#####################################################################
# Part 4 improved
#####################################################################
def generate_moves_midgame_endgame_improved(board):
    return generate_add(board)

def static_estimation_opening_improved(board):
    c= Counter(board)
    piecediff = c['W'] - c['B']
    whiteMobility = len(get_all_possible_moves(board, 'W', 'opening'))
    blackMobility = len(get_all_possible_moves(board, 'B', 'opening'))
    return piecediff + 0.4 * (whiteMobility - blackMobility)

def static_estimation_midgame_endgame_improved(board):
    c = Counter(board)
    white_num = c['W']
    black_num = c['B']
    piecediff = white_num - black_num
    whiteMobility = len(get_all_possible_moves(board, 'W', 'midgame'))
    blackMobility = len(get_all_possible_moves(board, 'B', 'midgame'))
    return int(piecediff + (whiteMobility - blackMobility))

def get_all_possible_moves(board, player, phase = 'opening'):
    moves = []
    if phase == 'opening':
        # In the opening phase, all empty spots are potential moves
        for i, spot in enumerate(board):
            if spot == 'x':  
                moves.append(i) 
    else:
        # In midgame/endgame, moves depend on the player's pieces
        for i, spot in enumerate(board):
            if spot == player:
                if player_has_only_three_pieces(board, player):  
                    # Player can jump to any empty spot
                    for j, potential_spot in enumerate(board):
                        if potential_spot == 'x':
                            moves.append((i, j))  # Move from i to j
                else:
                    # Move to adjacent spots
                    for adj in get_neighbors(i): 
                        if board[adj] == 'x':
                            moves.append((i, adj))  # Move from i to adj
    return moves

def player_has_only_three_pieces(board, player):
    return board.count(player) == 3

def generate_add_improved(board, transposition_table=None):
    """
    Generates all possible moves by adding 'W' to the board and handles mill creation.
    
    Parameters:
    board (list): The current state of the board.
    transposition_table (dict): A dictionary to store previously computed board states.
    
    Returns:
    list: A list of new board states after adding 'W'.
    """
    if transposition_table is None:
        transposition_table = {}

    board_tuple = tuple(board)
    if board_tuple in transposition_table:
        return transposition_table[board_tuple]

    l1 = []
    for i, piece in enumerate(board):
        if piece == 'x':  # If the spot is empty
            board[i] = 'W'  # Temporarily place 'W' to simulate the move
            if check_for_mills(i, board):
                # If placing 'W' here creates a mill, handle mill removal
                l1.extend(generate_remove_improved(board, i, transposition_table))  # Pass the index where the mill was created
            else:
                # If no mill is created, add the board state to the list
                l1.append(board.copy())  # Make a copy of the board for the list
            board[i] = 'x'  # Undo the move for the next iteration

    # Sort the moves based on their static evaluation scores
    l1.sort(key=lambda b: static_estimation_opening_improved(b, transposition_table), reverse=True)

    transposition_table[board_tuple] = l1
    return l1

def generate_remove_improved(board, index, transposition_table):
    """
    Removes 'B' pieces from the board that are not part of a mill.
    
    Parameters:
    board (list): The current state of the board.
    index (int): The index where the mill was created.
    transposition_table (dict): A dictionary to store previously computed board states.
    
    Returns:
    list: Updated list with new board states.
    """
    board_tuple = tuple(board)
    if board_tuple in transposition_table:
        return transposition_table[board_tuple]

    count = 0
    new_boards = []
    for i, piece in enumerate(board):
        if piece == 'B':
            if not check_for_mills(i, board):
                new_board = board.copy()
                new_board[i] = 'x'
                new_boards.append(new_board)
                count += 1

    if count == 0:
        new_boards.append(board.copy())

    transposition_table[board_tuple] = new_boards
    return new_boards

def static_evaluation_opening_improved(board, transposition_table=None):
    """
    Evaluates the board state and returns a score.
    
    Parameters:
    board (list): The current state of the board.
    transposition_table (dict): A dictionary to store previously computed board states.
    
    Returns:
    int: The evaluation score of the board.
    """
    if transposition_table is None:
        transposition_table = {}

    board_tuple = tuple(board)
    if board_tuple in transposition_table:
        return transposition_table[board_tuple]

    score = 0
    for piece in board:
        if piece == 'W':
            score += 1  # Each 'W' piece adds to the score
        elif piece == 'B':
            score -= 1  # Each 'B' piece subtracts from the score

    # Store the computed score in the transposition table
    transposition_table[board_tuple] = score
    return score