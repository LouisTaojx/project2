class BoardOut:
    def __init__(self):
        self.count = 0
        self.val = 0
        self.list = []

class PosType:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return self.val

# Define the PosType instances
X = PosType('x')
W = PosType('W')
B = PosType('B')

class PosList:
    def __init__(self, ip=None):
        if ip is None:
            self.pos_list = [X for _ in range(18)]
        else:
            self.pos_list = [W if c == 'W' else B if c == 'B' else X for c in ip]

    def get_copy(self):
        arr = [pos.val for pos in self.pos_list]
        return PosList(arr)
    
    # return the num of pieces of a given type
    def get_piece_count(self, piece_type):
        return sum(1 for t in self.pos_list if hasattr(t, 'val') and t.val == piece_type)

    def swap(self):
        swapped = PosList()
        swapped.pos_list = [B if t == W else W if t == B else X for t in self.pos_list]
        return swapped

    def __str__(self):
        return ''.join(pos.val if hasattr(pos, 'val') else str(pos) for pos in self.pos_list)
    

def generate_add(board):
    list_ = []
    for i, p in enumerate(board.pos_list):
        #print(f"Value of p at iteration {i}: {type(p)}")
        if p.val == 'x':
            copy = board.get_copy()
            copy.pos_list[i] = 'W'
            if is_close_mill(i, copy):
                list_ = generate_remove(copy, list_)
            else:
                list_.append(copy)
    return list_

def generate_remove(board, l):
    count = 0
    for i, p in enumerate(board.pos_list):
        if p.val == 'B':
            if not is_close_mill(i, board):
                copy = board.get_copy()
                copy.pos_list[i] = 'x'
                l.append(copy)
                count += 1
    if count == 0:
        l.append(board)
    return l

def generate_hopping(board):
    list_ = []
    for i, p in enumerate(board.pos_list):
        if p.val == 'W':
            for j, q in enumerate(board.pos_list):
                if q.val == 'x':
                    copy = board.get_copy()
                    copy.pos_list[i] = 'x'
                    copy.pos_list[j] = 'W'
                    if is_close_mill(j, copy):
                        generate_remove(copy, list_)
                    else:
                        list_.append(copy)
    return list_

def generate_move(board):
    list_ = []
    for i, p in enumerate(board.pos_list):
        if p.val == 'W':
            neighbors = get_neighbors(i)
            for j in neighbors:
                tmp = board.pos_list[j]
                if tmp.val == 'x':
                    dup = board.get_copy()
                    dup.pos_list[i].val = 'x'
                    dup.pos_list[j].val = 'W'
                    if is_close_mill(j, dup):
                        generate_remove(dup, list_)
                    else:
                        list_.append(dup)
    return list_

def generate_moves_opening(board):
    return generate_add(board)

def static_estimation_for_opening(board):
    return board.get_piece_count('W') - board.get_piece_count('B')

def generate_moves_midgame_endgame(board):
    piece = board.get_piece_count('W')
    # print(type(board))
    # print(dir(board))
    if board.get_piece_count('W') == 3:
        return generate_hopping(board)
    else:
        return generate_move(board)

def static_estimation_midgame_endgame(board):
    white_num = board.get_piece_count('W')
    black_num = board.get_piece_count('B')
    list_ = generate_moves_midgame_endgame_for_black(board)
    num_black_moves = len(list_)
    if black_num <= 2:
        return 10000
    elif white_num <= 2:
        return -10000
    elif num_black_moves == 0:
        return 10000
    else:
        return 1000 * (white_num - black_num) - num_black_moves

def generate_moves_midgame_endgame_for_black(board):
    temp_board = board.swap()
    b_moves = generate_moves_midgame_endgame(temp_board)
    for i, move in enumerate(b_moves):
        b_moves[i] = move.swap()
    return b_moves

def generate_moves_opening_for_black(board):
    temp_board = board.swap()
    b_moves = generate_moves_opening(temp_board)
    for i, move in enumerate(b_moves):
        b_moves[i] = move.swap()
    return b_moves

def static_estimation_opening_improved(board):
    return board.get_piece_count('W') + possible_mill_count(board, 'W') - board.get_piece_count('B')

def static_estimation_midgame_endgame_improved(board):
    white_num = board.get_piece_count('W')
    black_num = board.get_piece_count('B')
    list_ = generate_moves_midgame_endgame_for_black(board)
    num_black_moves = len(list_)
    possible_mill_count_ = possible_mill_count(board, 'W')
    if black_num <= 2:
        return 10000
    elif white_num <= 2:
        return -10000
    elif num_black_moves == 0:
        return 10000
    else:
        return 1000 * (white_num + possible_mill_count_ - black_num) - num_black_moves

check_possible_mill = False

def possible_mill_count(board, t):
    count = 0
    for i, p in enumerate(board.pos_list):
        if p == t:
            global check_possible_mill
            check_possible_mill = True
            if check_for_mills(board, p, i):
                count += 1
    return count

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

def is_close_mill(i, b):
    t = b.pos_list[i]
    if t == 'x':
        return False
    else:
        return check_for_mills(b, t, i)

def check_for_mills(b, t, i):
    switcher = {
        0: is_a_mill(b, t, 2, 4),
        1: is_a_mill(b, t, 3, 5) or is_a_mill(b, t, 8, 17),
        2: is_a_mill(b, t, 0, 4),
        3: is_a_mill(b, t, 1, 5) or is_a_mill(b, t, 7, 14),
        4: is_a_mill(b, t, 0, 2),
        5: is_a_mill(b, t, 1, 3) or is_a_mill(b, t, 6, 11),
        6: is_a_mill(b, t, 5, 11) or is_a_mill(b, t, 7, 8),
        7: is_a_mill(b, t, 6, 8) or is_a_mill(b, t, 3, 14),
        8: is_a_mill(b, t, 6, 7) or is_a_mill(b, t, 1, 17),
        9: is_a_mill(b, t, 10, 11) or is_a_mill(b, t, 12, 15),
        10: is_a_mill(b, t, 9, 11) or is_a_mill(b, t, 13, 16),
        11: is_a_mill(b, t, 9, 10) or is_a_mill(b, t, 14, 17) or is_a_mill(b, t, 5, 6),
        12: is_a_mill(b, t, 13, 14) or is_a_mill(b, t, 9, 15),
        13: is_a_mill(b, t, 12, 14) or is_a_mill(b, t, 10, 16),
        14: is_a_mill(b, t, 12, 13) or is_a_mill(b, t, 11, 17) or is_a_mill(b, t, 3, 7),
        15: is_a_mill(b, t, 16, 17) or is_a_mill(b, t, 9, 12),
        16: is_a_mill(b, t, 15, 17) or is_a_mill(b, t, 10, 13),
        17: is_a_mill(b, t, 15, 16) or is_a_mill(b, t, 11, 14) or is_a_mill(b, t, 1, 8),
    }
    return switcher.get(i, False)

def is_a_mill(b, t, i, i1):
    global check_possible_mill
    if check_possible_mill:
        check_possible_mill = False
        return (b.pos_list[i] == 'x' or b.pos_list[i] == t) and \
            (b.pos_list[i1] == 'x' or b.pos_list[i1] == t)
    return b.pos_list[i] == t and b.pos_list[i1] == t