import random
from typing import Tuple

from advsearch.your_agent import mcts
from advsearch.your_agent import iterative_deepening_search_w_hash
from advsearch.your_agent import othello_minimax_custom
from ..othello.gamestate import GameState
from ..othello.board import Board
from typing import Tuple, Callable


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
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.
    Board = state.get_board()

    global player_ai 
    player_ai = state.player
    
    if((Board.num_pieces('W') + Board.num_pieces('B') < 40) or (Board.num_pieces('W') + Board.num_pieces('B') >= 62)):
        return othello_minimax_custom.make_move(state)
    else:
        return mcts.monte_carlo(state, 3, 4.8, evaluate_count)


def evaluate_custom(state) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    # substitua pelo seu codigo                      #mobility heuristic - nro de jogadas possiveis
    board = state.get_board()
    white = board.num_pieces('W')
    black = board.num_pieces('B')
    if(state.is_terminal()):
        if(player_ai == 'W'):
            if(state.winner() == 'B'):
                return -10000
            else:
                return 10000
        if(player_ai == 'B'):
            if(state.winner() == 'W'):
                return -10000
            else:
                return 10000
            
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


def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    best_move = minimax_alpha_beta(state, max_depth, True, eval_func)[1]
    return best_move

def minimax_alpha_beta(state, max_depth:int, isMax:bool, eval_func:callable, alpha=float('-inf'), beta=float('inf')):
    if(max_depth == 0) or (state.is_terminal()):
        return eval_func(state), None
    if isMax:
        value = float('-inf')
        
        possible_moves = order_possible_moves(state)#move ordering here
        possible_moves.sort(reverse=True)
        
        for value_order, move in possible_moves:
            next_node = state.next_state(move)

            temp = minimax_alpha_beta(next_node, max_depth - 1, not isMax, eval_func, alpha, beta)[0]
            if temp > value:
                value = temp
                best_move = move
            if value >= beta:
                break
            alpha = max(alpha, value)
    else:
        value = float('inf')
        
        possible_moves = order_possible_moves(state)#move ordering here
        possible_moves.sort(reverse=True)
        
        for value_order, move in possible_moves:
            next_node = state.next_state(move)
            
            temp = minimax_alpha_beta(next_node, max_depth - 1, not isMax, eval_func, alpha, beta)[0]
            if temp < value:
                value = temp
                best_move = move
            if value <= alpha:
                break
            beta = min(beta, value)
                
    return value, best_move

def order_possible_moves(state):
    moves = state.legal_moves()
    arr = [[0]]*len(moves)
    j = 0
    for i in moves:
        child = state.next_state(i)
        value = getBonus(child)
        arr[j] = (value, i)
        j += 1

    return arr

def getBonus(state):
    board = state.get_board()
    white = board.num_pieces('W')
    black = board.num_pieces('B')
        
    if(player_ai == 'W'):
        value = white - black
    if(player_ai == 'B'):
        value = black - white
         
    return value   

def evaluate_count(state) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on the number of pieces of each color.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    # substitua pelo seu codigo
    
    board = state.get_board()
    white = board.num_pieces('W')
    black = board.num_pieces('B')
        
    if(player_ai == 'W'):
        value = white - black
    if(player_ai == 'B'):
        value = black - white
         
    return value   