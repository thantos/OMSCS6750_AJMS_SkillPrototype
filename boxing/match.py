import boxer
import announcer
import numpy as np
from boxing_strings import *


def initialize(game_state):
    game_state[NUMROUNDS] = 3

    game_state[PLAYERHP] = 20
    game_state[PLAYERSTAMINA] = 10
    game_state[PLAYERHISTORY] = []
    game_state[PLAYERBONUS] = ''

    game_state[OPPONENTHP] = 20
    game_state[OPPONENTSTAMINA] = 10
    game_state[OPPONENTHISTORY] = []
    game_state[OPPONENTBONUS] = ''

    game_state[ANNOUNCE] = ANNOUNCEIntro
    game_state[TOPICS] = [[],[]]

    # each round is a random length of turns ~ 6 on average
    game_state[TURNS] = map(int, np.random.normal(6, 1.25, game_state[NUMROUNDS]))
    game_state[CURRENTROUND] = 1
    game_state[CURRENTTURN] = 1

    return game_state


def update(game_state_prev):
    # the first time through we won't have any game state
    # initialize and return the game
    if PLAYERHP not in game_state_prev:
        return initialize(game_state_prev)

    # copy the game state
    game_state = dict(game_state_prev)

    game_state = resolve_turn(game_state)

    game_state = announcer.prompt(game_state)

    game_state = announcer.topics(game_state_prev, game_state)

    return game_state


def resolve_turn(game_state):
    # calculate the effect of each action
    phit, player_cost, damage_from_player = boxer.hit(game_state, player=True)
    ohit, opp_cost, damage_from_opp = boxer.hit(game_state, player=False)

    # apply the result of each action
    game_state[PLAYERHP] += player_cost[0] + damage_from_opp[0]
    game_state[PLAYERSTAMINA] += player_cost[1] + damage_from_opp[1]
    game_state[PLAYERHISTORY] += [(game_state[PLAYERMOVE], phit)]

    game_state[OPPONENTHP] += opp_cost[0] + damage_from_player[0]
    game_state[OPPONENTSTAMINA] += opp_cost[1] + damage_from_player[1]
    game_state[OPPONENTHISTORY] += [(game_state[OPPONENTMOVE], ohit)]

    # check for bonuses
    game_state[PLAYERBONUS] = boxer.bonus(game_state, player=True)
    game_state[OPPONENTBONUS] = boxer.bonus(game_state, player=False)

    return game_state
