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
    # calculate the effect of each action
    phit, player_cost, damage_from_player = boxer.hit(game_state, player=True)
    ohit, opp_cost, damage_from_player = boxer.hit(game_state, player=False)

    # apply the result of each action
    game_state[PLAYERHP] += player_cost[0] + damage_from_player[0]
    game_state[PLAYERSTAMINA] += player_cost[1] + damage_from_player[1]
    game_state[OPPONENTHP] += opp_cost[0] + damage_from_player[0]
    game_state[OPPONENTSTAMINA] += opp_cost[1] + damage_from_player[1]
    game_state[PLAYERHISTORY] += [(game_state[PLAYERMOVE], phit)]
    game_state[OPPONENTHISTORY] += [(game_state[OPPONENTMOVE], ohit)]

    # check for bonuses
    game_state[PLAYERBONUS] = boxer.bonus(game_state, player=True)
    game_state[OPPONENTBONUS] = boxer.bonus(game_state, player=False)

    return game_state
