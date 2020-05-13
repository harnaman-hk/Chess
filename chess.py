def process_moves(moves):
    '''
    This function breaks each sequence in the list of all_moves into black or white move depending on the course of game.
    It then passes the respective moves to make_move() for the moves to be updated on the board.
    '''
    for move in moves:
        if is_pawn_move(move):
            return True
        if is_capture(move):
            return True
        if is_castling(move):
            return True
        make_move(move,move[0],move[1])

def setup():
    '''
    Initialises the chess board to default state before the game begins
    '''
    squares = [y+x for x in '12345678' for y in 'abcdefgh']
    start = 'RNBQKBNR' + 'P'*8 + " "*32+'p'*8 + 'rnbqkbnr'

    board_view = {square: piece for square, piece in zip(squares, start)}
    piece_view = {_: [] for _ in "BKNPQRbknpqr"}
    for sq in board_view:
        piece = board_view[sq]
        if not piece == " ":
            piece_view[piece].append(sq)
    return board_view, piece_view

# def move(action):
#     piece, extra, final_pos = action[0], action[1:-2], action[-2::]
#     if extra == "":
#         if len(piece_view[piece] == 1):
#             make_move(piece, piece_view[piece][0], final_pos)
#         else:
#             print("-------error--------")


def castle(move, board_view, piece_view):
    '''
    This function performs the castling move, both the king side casting and queen side castling.
    An updated version of the board.
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
    '''
    ``return type: bool``
    returns True if there is no obstruction on board between a and b
    '''
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
    '''
    :param move: move in play
    :param board_view: position of pieces on board

    ``return type: str`` 
    
    returns the initial position of a piece given its final position
    '''
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
    '''
    :param piece: chess piece to be moved in the current move
    :param move_from: initial position of piece
    :param move_to: final position of piece

    Update the board and piece statistics with the current move in play
    '''
    board_view[move_from] = SPACE
    board_view[move_to] = piece
    piece_view[piece].append(move_to)
    piece_view[piece].remove(move_from)


def is_pawn_move(move):
    '''
    ``return type: bool`` 
    
    returns True if the move in play is a pawn move
    '''
    return move[0] in 'pP'


def is_capture(move):
    '''
    ``return type: bool`` 
    
    returns True if the move in play is a capture move
    '''
    return 'x' in move


def is_castling(move):
    '''
    ``return type: bool`` 
    
    returns True if the move in play is a Castling move (King side or Queen side Castling)
    '''
    return move in "oooOOO"

if __name__ == "__main__":
    from PgnParser import setup, pgn_to_moves

    game_file = 'game.txt'

    board_view, piece_view = setup()
    moves = pgn_to_moves(game_file)
    MOVE_BY_MOVE = False
    WHITE = 1
    BLACK = 8
    SPACE = " "
