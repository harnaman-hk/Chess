import re

'''
Read the pgn file provided by the user and pre process the file to extract meaningful data, i.e. moves
'''


def pgn_to_moves(game_file):
    '''
    Reads a ``.pgn`` file.
    Further, beggining remarks, comments, indexing, etc are removed from the input so that only the moves processed further.
    '''
    raw_moves = SPACE.join([line.strip() for line in open(game_file)])

    # remove beginning information lines i.e. text within []
    text_marked = raw_moves.replace("[", "<").replace("]", ">")
    text = re.compile("<.*>")
    text_removed = re.sub(text, SPACE, text_marked)

    # remove comments
    comments_marked = text_removed.replace("{", "<").replace("}", ">")
    comments_to_remove = re.compile("<[^>]*>")
    comments_removed = re.sub(comments_to_remove, " ", comments_marked)

    # remove index of moves
    index_label = re.compile("[1-9][0-9]*\s*\.")
    all_moves = [_.strip() for _ in index_label.split(comments_removed)]
    last_move = all_moves[-1]
    result = re.compile("\s*\**1*/*2*-*1*/*2*0*")
    last_move = result.sub("", last_move)
    return pre_process_moves(all_moves[1:-1]) + [pre_process_last_move(last_move)]


def pre_process_moves(moves):
    '''
    ``return type: list[ str ]``
    returns a list of sequence of black, white moves in a game
    '''
    return [pre_process_a_move(one_move) for one_move in moves]


def pre_process_a_move(move):
    '''
    ``return type: str``
    add 'P' for pawn move
    capital notations for white pieces, small for black
    '''
    wmove, bmove = move.split()
    if wmove[0] in 'abcdefgh':
        wmove = 'P' + wmove
    if bmove[0] in 'abcdefgh':
        bmove = 'p' + bmove
    bmove = bmove.lower()
    return clean(wmove)+SPACE+clean(bmove)


def pre_process_last_move(move):
    '''
    ``return type: str``
    As the last move may contain extra information regarding the result of a match, it is handled separately.
    All data except the move is removed.
    '''
    move = move.strip()
    if SPACE in move:
        return pre_process_a_move(move)
    if move[0] in 'abcdefgh':
        move[0] = 'P' + move[0]
    return move


def clean(move):
    '''
    ``return type: str``
    Each move is filtered to remove any data other than Alpha-numeric characters
    '''
    return ''.join(filter(str.isalnum, move))


if __name__ == "__main__":
    FILES = "abcdefgh"
    RANKS = "12345678"
    SPACE = " "
    EnPassant = "e.p."
    moves = pgn_to_moves(r'game.txt')
    print(moves)
