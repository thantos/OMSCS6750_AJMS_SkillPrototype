from boxing_strings import *

def build(game_state):

    prompt = game_state[ANNOUNCE]

    if ANNOUNCEIntro in prompt:
        return build_intro(game_state)
    elif ANNOUNCEMidround in prompt:
        return build_midround(game_state)
    elif ANNOUNCEBetweenRound in prompt:
        return build_betweenround(game_state)
    else:
        return build_gameover(game_state)

def build_intro(game_state):
    pass

def build_midround(game_state):
    pass

def build_betweenround(game_state):
    pass

def build_gameover(game_state):
    pass