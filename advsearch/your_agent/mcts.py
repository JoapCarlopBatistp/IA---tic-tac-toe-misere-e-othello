import random
import time
from typing import Tuple


# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.
def heuristic_function(state):
    board = state.get_board()
    white = board.num_pieces('W')
    black = board.num_pieces('B')
        
    if(player_ai == 'W'):
        value = white - black
    if(player_ai == 'B'):
        value = black - white
    return value

def make_move(state, max_depth:int = 5, eval_func:callable = heuristic_function, time_limit:float = 4.8) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    global player_ai
    player_ai = state.player
    move = monte_carlo(state, max_depth, time_limit, eval_func)
    return move

def has_time(time_limit, start_time):
    if (start_time + time_limit) < time.time():
        return False
    return True

def monte_carlo(state, max_depth, time_limit, eval_func):
    start_time = time.time()
    depth = 0
    legal_moves = state.legal_moves()
    prince_of_monaco = (-1, -1)
    max_reward = float('-inf')
    i = 0
    while has_time(time_limit, start_time) and i < len(list(legal_moves)):
        reward = mcr(state, list(legal_moves)[i], depth, max_depth, time_limit, start_time, eval_func)
        if reward > max_reward:
            prince_of_monaco = list(legal_moves)[i]
            max_reward = reward
        i += 1
    return prince_of_monaco

def mcr(state, move, depth, max_depth, time_limit, start_time, eval_func):
    depth += 1
    if not has_time(time_limit, start_time):
        return float('-inf')
    elif depth == max_depth:
        return eval_func(state)
    elif state.is_terminal():
        return eval_func(state) * 10
    else:
        next_state = state.next_state(move)
        legal_moves = next_state.legal_moves()
        acc_reward = 0.0
        for move in legal_moves:
            acc_reward += mcr(next_state, move, depth, max_depth, time_limit, start_time,eval_func)
        return acc_reward

