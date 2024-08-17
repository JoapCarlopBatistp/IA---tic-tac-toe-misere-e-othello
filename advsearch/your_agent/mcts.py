import random
import psutil
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
    # Remova-o e coloque a sua implementacao do MCTS

    return (-1, -1)

def monte_carlo_tree_search():
    return 0

def selection():
    return 0

def ucb():
    return 0

def expansion():
    return 0

def rollout():
    return 0

def backpropagation():
    return 0

def resources_left(time:float):
    memory = psutil.virtual_memory()
    ram_used = memory[3]/1000000000
    if(ram_used > 3.50 and time > 4.80):
        return False
    
    return True
