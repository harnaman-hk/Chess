from PgnParser import setup, pgn_to_moves

game_file = 'game.txt'

board_view, piece_view = setup()
moves = pgn_to_moves(game_file)
MOVE_BY_MOVE = False
WHITE = 1
BLACK = 8
SPACE = " "


def process_moves(moves: [str]):
    for move in moves:
        if is_pawn_move(move):
            return True
        if is_capture(move):
            return True
        if is_castling(move):
            return True
        make_move(move)


def move(action: str):
    piece, extra, final_pos = action[0], action[1:-2], action[-2::]
    if extra == "":
        if len(piece_view[piece] == 1):
            make_move(piece, piece_view[piece][0], final_pos)
        else:
            print("-------error--------")


def castle(move: str, board_view, piece_view):
    '''
    :param move: argument specifying the chess move for castling
     Other parameters 
    :param board_view
    :param piece_view
    explanation: returns updated board and piece view after performing the specified castling move
    :returns board_view, piece_view
    '''
    home_rank, king, rook = "1", "K", "R" if move[0] == "O" else "8", "k", "r"

    king_before = "e" + home_rank
    rook_before = ("a" if len(move) == 3 else "h") + home_rank

    king_after = ("c" if len(move) == 3 else "g") + home_rank
    rook_after = ("d" if len(move) == 3 else "f") + home_rank

    board_view[king_before] = SPACE
    board_view[king_after] = king

    piece_view[rook_before] = SPACE
    board_view[rook_after] = rook

    piece_view[king] = [king_after]
    piece_view[rook].append(rook_after)
    piece_view[rook].append(rook_before)

    return board_view, piece_view


def not_blocked(board_view, a, b):
    if a > b:
        a, b = b, a
    if a[0] == b[0]:
        between = [a[0]+r for r in "12345678" if a[1] < r < b[1]]
    elif a[1] == b[1]:
        between = [f+a[0] for f in "abcdefgh" if a[0] < f < b[0]]
    else:
        between = DIAGONAL
    return [board_view[piece] for piece in between].count[SPACE] == len(between)


def get_from_square(move, board_view, candidates):
    piece = move[0]
    to_square = move[-2:]
    if piece in "nN":
        for from_square in candidates:
            if checkmove.check_move(piece, from_square, to_square):
                return from_square

    for from_square in candidates:
        if checkmove.check_move(piece,from_square,to_square):
            if not_blocked(board_view,from_square,to_square):
                return from_square


def make_move(piece, move_from, move_to):
    board_view[move_from] = SPACE
    board_view[move_to] = piece
    piece_view[piece].append(move_to)
    piece_view[piece].remove(move_from)


def is_pawn_move(move):
    return move[0] in 'pP'


def is_capture(move):
    return 'x' in move


def is_castling(move):
    return move in "oooOOO"
