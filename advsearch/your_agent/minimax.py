import random
from typing import Tuple, Callable

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
    global player_ai
    player_ai = state.player
    best_move = minimax_alpha_beta(state, max_depth, True, eval_func)[1]
    return best_move

def minimax_alpha_beta(state, max_depth:int, isMax:bool, eval_func:callable, alpha=float('-inf'), beta=float('inf')):
    if(max_depth == 0) or (state.is_terminal()):
        return eval_func(state, player_ai), None
    if isMax:
        value = float('-inf')
        for move in state.legal_moves():
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
        for move in state.legal_moves():
            next_node = state.next_state(move)
            
            temp = minimax_alpha_beta(next_node, max_depth - 1, not isMax, eval_func, alpha, beta)[0]
            if temp < value:
                value = temp
                best_move = move
            if value <= alpha:
                break
            beta = min(beta, value)
                
    return value, best_move