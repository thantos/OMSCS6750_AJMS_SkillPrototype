import random
import boxer
import numpy as np
from boxing_strings import *


def initialize(game_state):
    game_state[PLAYERHP] = 20
    game_state[PLAYERSTAMINA] = 10
    game_state[PLAYERHISTORY] = []
    game_state[PLAYERBONUS] = ''

    game_state[OPPONENTHP] = 20
    game_state[OPPONENTSTAMINA] = 10
    game_state[OPPONENTHISTORY] = []
    game_state[OPPONENTBONUS] = ''

    # each round is a random length of turns ~ 6 on average
    game_state[TURNS] = map(int, np.random.normal(6, 1.25, MAX_ROUNDS))

    return game_state


def update(game_state):
    return resolve_turn(game_state)


def resolve_turn(game_state):
    opp_move = boxer.random_move()
    game_state[OPPONENTMOVE] = opp_move

    phit, pp, po = boxer.hit(game_state, player=True)
    ohit, oo, op = boxer.hit(game_state, player=False)

    game_state[PLAYERHP] += pp[0] + op[0]
    game_state[PLAYERSTAMINA] += pp[1] + op[1]

    game_state[OPPONENTHP] += oo[0] + po[0]
    game_state[OPPONENTSTAMINA] += oo[1] + po[1]
    game_state[PLAYERHISTORY] += [(game_state[PLAYERMOVE], phit)]
    game_state[OPPONENTHISTORY] += [(game_state[OPPONENTMOVE], ohit)]
    return game_state
