import random
import time
import psutil
from typing import Tuple
from numpy import log as ln

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
    # Remova-o e coloque a sua implementacao do MCTS
    initial_time = time.time()
    time_limit = 4.8
    end_time = initial_time + time_limit

    return monte_carlo_tree_search(state, end_time)

def monte_carlo_tree_search(state, end_time):
    child_rewards = []
    while(resources_left(end_time)):
    #selection and expansion
        child = rollout(state)
        if(not child.is_terminal()):
    #simulate
            reward = simulate(state, child)

    return reward

#def uct():
#    return 0

def simulate(state, next_state):
    cumulative_reward = 0.0
    depth = 0
    while(not next_state.is_terminal()):
        action = rollout(state)
        
        cumulative_reward += simulate(next_state, action)
        cumulative_reward += 2 * (2 * ln(state.visit_count)/state.visit_count)
        depth += 1
        
    return cumulative_reward

def rollout(state):
    moves = state.legal_moves()
    child = state.next_state(random.choice(moves))
    return child


def resources_left(end_time:float):
    if(time.time() >= end_time):
        return False
    
    return True
