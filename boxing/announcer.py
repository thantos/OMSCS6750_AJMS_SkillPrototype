from boxing_strings import *


def prompt(game_state):
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


def topics(game_state_prev, game_state):
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
        turns_in_final_round = game_state[TURNS][n_rounds - 1]
        if turn == turns_in_final_round:
            return True

    return False


def round_over(game_state):
    round = game_state[CURRENTROUND]

    turn = game_state[CURRENTTURN]
    turns_in_round = game_state[TURNS][round - 1]

    return turn == turns_in_round
