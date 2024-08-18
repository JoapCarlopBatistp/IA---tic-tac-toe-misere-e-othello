import time
from typing import Tuple
from typing import Tuple, Callable
from operator import itemgetter, xor


winCutoff = 5000
UPPERBOUND = 1
LOWERBOUND = -1
EXACT_MATCH = 0

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
    global tts
    tts = hashtable()
    max_score = float('-inf')
    player_ai = state.player
    timelimit = 4.5
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
    
    hash_move = None
    hash_entry = tts.get(state)
    if hash_entry:
        hash_depth, hash_move, hash_alpha, hash_beta, hash_type = hash_entry
        if(hash_depth >= max_depth):
            if(hash_type == EXACT_MATCH):
                return hash_alpha, hash_move
            if(hash_type == LOWERBOUND):
                alpha = max(alpha, hash_alpha)
            if(hash_type == UPPERBOUND):
                beta = min(beta, hash_alpha)
            
            if(alpha >= beta):
                return hash_alpha, hash_move
    
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
    
    if(value <= alpha):
            hash_type = UPPERBOUND
    elif(value >= beta):
            hash_type = LOWERBOUND
    else:
            hash_type = EXACT_MATCH
            
    
    hash_depth = max_depth        
    tts.add_in_hash(state, hash_depth, best_move, alpha, beta, hash_type)
            
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
    
    w1 = 0.2
    pieces_cardinality = 0
    w2 = 0.8
    board_mask_value = 0
    w3 = 3
    stability = 0
    w4 = 0.2
    mobility = 0
    
    
    #diferença de peças
    if(player_ai == 'W'):
        pieces_cardinality = white - black
    if(player_ai == 'B'):
        pieces_cardinality = black - white
    
    #máscara
    size_board = len(board.tiles)
    
    for row in range(size_board):
        for collumn in range(size_board):
            if (board.tiles[row][collumn] == player_ai):
                board_mask_value += EVAL_TEMPLATE[row][collumn]
                stability += stability_calculation(row, collumn, size_board)
            elif (board.tiles[row][collumn] == board.opponent(player_ai)):
                board_mask_value -= EVAL_TEMPLATE[row][collumn]
                stability -= stability_calculation(row, collumn, size_board)
                
    #mobilidade
    white = len(board.legal_moves('W'))
    black = len(board.legal_moves('B'))
        
    if(player_ai == 'W'):
        mobility += white - black
    if(player_ai == 'B'):
        mobility += black - white
        
    return (w1*pieces_cardinality + w2*board_mask_value + w3*stability + w4*mobility)

def stability_calculation(row, collumn, size_board):
    value = 0
    if row == 0 or row == size_board - 1 or collumn == 0 or collumn == size_board - 1:
        value += 1

        # Adicionar valor às peças estáveis nas diagonais
    if (row == 0 and collumn == 0) or (row == 0 and collumn == size_board - 1) or (row == size_board - 1 and collumn == 0) or (row == size_board - 1 and collumn == size_board - 1):
        value += 2
        
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
        i = 0
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
    
    def add_in_hash(self, state, hash_depth, hash_move, hash_alpha, hash_beta,hash_type):
        h = self.get_hash(state)
        values = [hash_depth, hash_move, hash_alpha,hash_beta,hash_type]
        self.arr[h] = values
    
    def get(self, state):
        h = self.get_hash(state)
        resultado = self.arr[h]
        return resultado
    
