import random
import boxer
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

    game_state[ANNOUNCEPrompt] = ANNOUNCEIntro

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

    game_state = resolve_turn(game_state_prev)

    game_state = announcer_prompt(game_state)

    # game_state = announcer_topics(game_state_prev, game_state)

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


def announcer_prompt(game_state):
    prompt = ANNOUNCEMidround
    if game_over(game_state):
        prompt = ANNOUNCEGameOver
    elif round_over(game_state):
        prompt = ANNOUNCEBetweenRound
        game_state[CURRENTTURN] = 1
        game_state[CURRENTROUND] += 1
    else:
        game_state[CURRENTTURN] += 1

    game_state[ANNOUNCEPrompt] = prompt

    return game_state

def announcer_topics(game_state_prev, game_state):
    pass




def game_over(game_state):
    if game_state[PLAYERHP] <= 0:
        return True
    if game_state[OPPONENTHP] <= 0:
        return True

    round = game_state[CURRENTROUND]
    n_rounds = game_state[NUMROUNDS]
    if round == n_rounds:

        turn = game_state[CURRENTTURN]
        turns_in_final_round = game_state[TURNS][n_rounds-1]
        if turn == turns_in_final_round:
            return True

    return False


def round_over(game_state):
    round = game_state[CURRENTROUND]

    turn = game_state[CURRENTTURN]
    turns_in_round = game_state[TURNS][round-1]

    return turn == turns_in_round
