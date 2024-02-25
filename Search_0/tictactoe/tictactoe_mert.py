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
    countX=0
    countO=0
    
    #hamle tahtadaki hamle sayısını say
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                countX+=1
            if board[row][col] == O:
                countO+=1
    
    #hamle sırası kimde 
    if countO <countX:
        return O
    elif countX<countO:
        return X
    else:
        return X
    



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_possible_actions = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col]== EMPTY:
                all_possible_actions.add((row,col))
                
    return all_possible_actions 
                
                


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("İNVALİD ACTİON")
    
    row,col =action
    board_copy=copy.deepcopy(board)
    board_copy[row][col]=player(board)
    
    return board_copy

def check_row(board,player):
    for row in range(len(board)):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player :
            return True
    return False
        
def check_col(board,player):
    for col in range(len(board)):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player :
            return True
    return False
        
def check_dig1(board,player):
    count=0
    for  row in range(len(board)):
            if board[row][row] ==player:
                count+=1
    if count==3:
        return True
    else:   
        return False

def check_dig2(board,player):
    count=0 
    for  row in range(len(board)):
        if board[row][len(board[row])-1 -row ]==player:
            count+=1
    if count==3:
        return True
    else:   
        return False



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_row(board,X) or check_col(board,X) or check_dig1(board,X) or check_dig2(board,X):
        return X
    elif check_row(board,O) or check_col(board,O) or check_dig1(board,O) or check_dig2(board,O):    
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) !=None:
        return True
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col]==EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner (board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else:    
        return 0
    
def max_value(board):
    v=-math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v=max(v,min_value(result(board,action)))
    return v

def min_value(board):
    v=math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v=min(v,max_value(result(board,action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    #CASE Player X Turn (Max-player)
    if player(board)==X:
        plays=[]
        #olası hamleler için döngü
        for action in actions(board):
            #yapılan hamlenin min puanı ile aksiyonu bir tuple a ekleyip plays listesine ekliyoruz
            plays.append([min_value(result(board,action)),action]) #----min_value
    
        #en yüksek puanlı hamleyi seçmek için listeyi ters çevirip ilk elemenı alıyoruz
        return sorted(plays,key=lambda x:x[0],reverse=True)[0][1]
    
    #CASE Player O Turn (Min-player)
    if player(board)==O:
        plays=[]
        #olası hamelr için döngü
        for action in actions(board):
            #yapılan hamlenin max puanı ile aksiyonu bir tuple a ekleyip plays listesine ekliyoruz
            plays.append([max_value(result(board,action)),action])    #----max_value
        
        return sorted(plays,key=lambda x:x[0])[0][1]  #----
            
            
            
            
            
            
            
            
            
            