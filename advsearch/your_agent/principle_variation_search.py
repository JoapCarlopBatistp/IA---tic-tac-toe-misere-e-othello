import random
from typing import Tuple

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo retorna uma jogada ilegal
    # Remova-o e coloque a sua implementacao do 
    global player_ai
    player_ai = state.player
    best_move = pvs(state, 100, 1, eval_func)[1]
    return best_move

def pvs(state, max_depth:int, color:int, eval_func:callable, alpha=float('-inf'), beta=float('inf')):
    if(max_depth == 0) or (state.is_terminal()):
        return color * eval_func(state, player_ai), None
    for move in state.legal_moves():
        child = state.next_state(move)
        if isFirst(child):
            best_move = move
            score = -pvs(child, max_depth - 1, -color, eval_func, -beta, -alpha)[0]
        else:
            score = -pvs(child, max_depth - 1, -color, eval_func, -alpha - 1, -alpha)[0]
            if(alpha < score and score < beta):
                score = -pvs(child, max_depth - 1, -color, eval_func, -beta, -alpha)[0]
        alpha = max(alpha, score)
        if(alpha >= beta):
            break
    return alpha, best_move

def isFirst():
    return 0


def eval_func():
    #heuristicas do pvs
    return 0