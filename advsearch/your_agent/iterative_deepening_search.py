import time
from typing import Tuple
from typing import Tuple, Callable
from operator import itemgetter, xor


winCutoff = 5000


EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30, 100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30, 100]
]

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    global max_score
    global player_ai
    tts = hashtable()
    max_score = float('-inf')
    player_ai = state.player
    timelimit = 4.8
    result = iterative_deepening_search(state, timelimit)
    
    if(result[0] >= winCutoff):
        return result[1]
    
    if(result[0] > max_score):
        max_score = result[0]
        best_move = result[1]
        
    return best_move

def iterative_deepening_search(state, timelimit:float):
    start_time = time.time()
    end_time = start_time + timelimit
    depth = 1
    score = 0
    search_cutoff = False
    while(True):
        if(time.time() >= end_time):
            break
        
        search_result = minimax_move(state, depth, eval_func, end_time)

        if(score >= winCutoff):
            return search_result
        
        if(not search_cutoff):
            score = search_result[0]
            move = search_result[1]
        
        depth += 1
        
    return score, move


def minimax_move(state, max_depth:int, eval_func:Callable, end_time) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    result = minimax_alpha_beta(state, max_depth, True, eval_func, end_time)
    return result

def minimax_alpha_beta(state, max_depth:int, isMax:bool, eval_func:callable, end_time,alpha=float('-inf'), beta=float('inf')):
    
    if(max_depth == 0) or (state.is_terminal() or time.time() >= end_time):
        return eval_func(state), None
    
    if isMax:
        value = float('-inf')
        for move in state.legal_moves():

            next_node = state.next_state(move)

            temp = minimax_alpha_beta(next_node, max_depth - 1, not isMax, eval_func, end_time, alpha, beta)[0]
            if temp > value:
                value = temp
                best_move = move
            if value >= beta:
                break
            alpha = max(alpha, value)
    else:
        value = float('inf')
        for move in state.legal_moves():
            next_node = state.next_state(move)
            
            temp = minimax_alpha_beta(next_node, max_depth - 1, not isMax, eval_func, end_time, alpha, beta)[0]
            if temp < value:
                value = temp
                best_move = move
            if value <= alpha:
                break
            beta = min(beta, value)
            
    return value, best_move

def getBonus(state):
    board = state.get_board()                  
    white = len(board.legal_moves('W'))
    black = len(board.legal_moves('B'))
        
    if(player_ai == 'W'):
        value = white - black
    if(player_ai == 'B'):
        value = black - white
         
    return value  


def eval_func(state):
    board = state.get_board()
    white = board.num_pieces('W')
    black = board.num_pieces('B')
        
    if(player_ai == 'W'):
        value = white - black
    if(player_ai == 'B'):
        value = black - white
         
    return value   

def initialize_zobrist_hash_Table():
    zTable = [[[None] * 2 for _ in range(8)] for _ in range(8)]
    currNumber = 0

    for row in range(8):
        for col in range(8):
            for i in range(2):
                zTable[row][col][i] = currNumber
                currNumber += 1

    return zTable

class hashtable():
    def __init__(self):
        self.max = 10000000
        self.arr = [None for i in range(self.max)]
        self.ztable = initialize_zobrist_hash_Table()

    def get_hash(self, state):
        board = state.get_board()
        tabuleiro = board.__str__()
        h = 0
        for row in self.ztable:
            for element in row:
                match (tabuleiro[i]):
                    case 'B':
                        h = xor(h, element[0])
                    case 'W':
                        h = xor(h, element[1])
                i += 1
                while((tabuleiro[i] == chr(10)) and i < 70):
                    i += 1
    
        return h
    
    def add_in_hash(self, state, values):
        h = self.get_hash(state)
        self.arr[h] = values
    
    def get(self, state):
        h = self.get_hash(state)
        resultado = self.arr[h]
        return resultado
    
