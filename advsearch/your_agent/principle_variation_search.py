import random
from typing import Tuple
#NÃO COMPLETAMENTE IMPLEMENTADO!!!!

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.
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

    global player_ai
    global refutation_table
    player_ai = state.player
    refutation_table = create_refutation_table(3)
    best_move = pvs(state, 3, 1, eval_func)[1]
    return best_move

def pvs(state, max_depth:int, color:int, eval_func:callable, alpha=float('-inf'), beta=float('inf')):
    if(max_depth == 0) or (state.is_terminal()):
        return color * eval_func(state, player_ai), None
    move_list = []
    move_value = 0
    probably_best_move = -1, -1
    best_score = -101
    
    for move in state.legal_moves():
        curr_value = returnBonus(state,max_depth, move)
        move_list.append(move)
        if(move_value < curr_value):
            probably_best_move = move
            move_value =+ curr_value
        best_move = move
    move_list.sort()
    for estado in move_list:
        child = state.next_state(estado)
        if isFirst(estado, probably_best_move):
            best_move = estado
            score = -1 * pvs(child, max_depth - 1, -color, eval_func, -beta, -alpha)[0]
            best_score = score
        else:
            score = -1 * pvs(child, max_depth - 1, -color, eval_func, -alpha - 1, -alpha)[0]
            if(alpha < score and score < beta):
                score = -1 * pvs(child, max_depth - 1, -color, eval_func, -beta, -alpha)[0]
        if(best_score < score):
            best_move = estado
            best_score = score
        alpha = max(alpha, score)
        if(alpha >= beta):
            insert_in_refutation_table(refutation_table, max_depth, estado)
            break
    return alpha, best_move

def isFirst(child, probably_best_move):
    if(child == probably_best_move):
        return True
    else:
        return False

def returnBonus(state, max_depth,move:Tuple[int, int]):
    value = 0
    if(is_killer_move(max_depth,move)):
        value -= 1000
    value += mobility(state, move)
    value += count(state, move)
    
    return value

def is_killer_move(max_depth:int,move:Tuple[int, int]):
    if any((max_depth,(move)) in sublist for sublist in refutation_table):
        return True
    else:
        return False
    

def create_refutation_table(killer_moves_stored: int):
    refutation_table = [[0 for i in range(2)] for j in range(killer_moves_stored)]
    return refutation_table

def insert_in_refutation_table(refutation_table, depth: int, killer_move:Tuple[int, int]):
    if(any((0, 0) in sublist for sublist in refutation_table)):
        refutation_table.insert(len(refutation_table), (depth, killer_move))
    else:
        refutation_table.pop(0)
        refutation_table.insert(len(refutation_table), (depth, killer_move))
        
    return refutation_table

def mobility(state, move:Tuple[int, int]):
    value = 0
    next_state = state.next_state(move)
    board = next_state.get_board()                  
    white = len(board.legal_moves('W'))
    black = len(board.legal_moves('B'))
        
    if(player_ai == 'W'):
        value = white - black
    if(player_ai == 'B'):
        value = black - white
         
    return value  

def count(state, move:Tuple[int, int]):
    next_state = state.next_state(move)
    board = next_state.get_board()
    white = board.num_pieces('W')
    black = board.num_pieces('B')
        
    if(player_ai == 'W'):
        value = white - black
    if(player_ai == 'B'):
        value = black - white
         
    return value   
def eval_func(state, player:str):
    board = state.get_board()
    tabuleiro = board.__str__()
    white = 0
    black = 0
    i = 0
    for row in EVAL_TEMPLATE:
        for element in row:
            match (tabuleiro[i]):
                case 'B':
                    black += element
                case 'W':
                    white += element
            i += 1
            while((tabuleiro[i] == chr(10)) and i < 70):
                i += 1
                
    if(player == 'W'):
        value = white - black
    if(player == 'B'):
        value = black - white
    
    return value