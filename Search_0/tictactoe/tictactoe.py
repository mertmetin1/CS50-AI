"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0
    
    # Count the number of X's and O's on the board
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                countX += 1
            elif board[row][col] == O:
                countO += 1
    
    # Check whose turn it is based on the counts
    if countO < countX:
        return O
    else:
        return X

def check_row(board, player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    return False

def check_col(board, player):
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False

def check_dig1(board, player):
    count = 0
    for row in range(len(board)):
        if board[row][row] == player:
            count += 1
    return count == 3

def check_dig2(board, player):
    count = 0 
    for row in range(len(board)):
        if board[row][len(board[row]) - 1 - row] == player:
            count += 1
    return count == 3

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in [X, O]:
        if (check_row(board, player) or check_col(board, player) or
            check_dig1(board, player) or check_dig2(board, player)):
            return player
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(all(cell is not None for cell in row) for row in board)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # CASE Player X Turn (Max-player)
    if player(board) == X:
        best_val = -math.inf
        best_move = None
        for action in actions(board):
            val = min_value(result(board, action))
            if val > best_val:
                best_val = val
                best_move = action
        return best_move
    
    # CASE Player O Turn (Min-player)
    else:
        best_val = math.inf
        best_move = None
        for action in actions(board):
            val = max_value(result(board, action))
            if val < best_val:
                best_val = val
                best_move = action
        return best_move

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                possible_actions.add((i, j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action")
    i, j = action
    player_turn = player(board)
    new_board = [row[:] for row in board]  # Create a copy of the board
    new_board[i][j] = player_turn
    return new_board
