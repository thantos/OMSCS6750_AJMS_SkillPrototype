import random
import csv
from boxing_strings import *
from modifiers import *


def hit(game_state, player=True):
    if player:
        player_move = game_state[PLAYERMOVE]
        opp_move = game_state[OPPONENTMOVE]
        bonus = game_state[PLAYERBONUS]
    else:
        player_move = game_state[OPPONENTMOVE]
        opp_move = game_state[PLAYERMOVE]
        bonus = game_state[OPPONENTBONUS]

    player_modifier = modifier(player_move, opp_move)
    does_hit = hit_success(bonus=bonus, modifier=player_modifier)
    player_delta, opp_delta = result(player_move, does_hit)
    return does_hit, player_delta, opp_delta


# roll a 20 sided dice return true if dice > threshold
# if player has advantage roll 2 dice and take best
# if player has disadvantage roll 2 dice and take worst
# if player has super auto hit
def hit_success(modifier, bonus, hit_threshold=7):
    if has_super(bonus):
        return True

    if has_exhausted(bonus):
        return False

    roll1 = (roll() + modifier) > hit_threshold
    roll2 = (roll() + modifier) > hit_threshold

    if has_advantage(bonus):
        return roll1 or roll2

    if has_disadvantage(bonus):
        return not (not roll1 or not roll2)

    return roll1


def result(move, does_hit):
    if does_hit:
        return hit_result(move)
    return miss_result(move)


def hit_result(move):
    if move == MOVEjab:
        return (0, 0), (-1, -1)
    if move == MOVEcross or move == MOVEhook:
        return (0, -1), (-3, 0)
    if move == MOVEuppercut:
        return (0, -2), (-5, -1)
    if move == MOVEwrapup:
        return (0, 1), (0, -1)
    if move == MOVEbob or move == MOVEfootwork:
        return (1, 0), (0, 0)
    if move == MOVEprotect or move == MOVEhandsup:
        return (0, 1), (0, 0)
    return (0, 0), (0, 0)


def miss_result(move):
    if move == MOVEjab:
        return (0, 0), (0, 0)
    if move == MOVEcross or move == MOVEhook:
        return (0, -1), (0, 0)
    if move == MOVEuppercut:
        return (0, -2), (0, 0)
    if move == MOVEwrapup:
        return (0, 1), (0, 0)
    if move == MOVEbob or move == MOVEfootwork:
        return (1, 0), (0, 0)
    if move == MOVEprotect or move == MOVEhandsup:
        return (0, 1), (0, 0)
    return (0, 0), (0, 0)


def has_advantage(bonus):
    if has_disadvantage(bonus):
        return False
    return ADadvantage in bonus


def has_disadvantage(bonus):
    return ADdisadvantage in bonus


def has_super(bonus):
    return ADsuper in bonus


def has_exhausted(bonus):
    return ADexhausted in bonus


def roll():
    return random.random() * 20


def random_move():
    moves = [MOVEjab, MOVEhook, MOVEcross, MOVEuppercut,
             MOVEfeint, MOVEtaunt, MOVEwrapup, MOVEbob,
             MOVEfootwork, MOVEhandsup, MOVEprotect]
    return random.choice(moves)


def bonus(game_state, player=True):
    if player:
        player_move, player_hit = game_state[PLAYERHISTORY][-1]
        opp_move, opp_hit = game_state[OPPONENTHISTORY][-1]
    else:
        player_move, player_hit = game_state[OPPONENTHISTORY][-1]
        opp_move, opp_hit = game_state[PLAYERHISTORY][-1]

    if MOVEuppercut in player_move:
        return ADdisadvantage

    if MOVEhook in player_move:
        return ADNobonus

    if MOVEcross in player_move:
        return ADNobonus

    if MOVEjab in player_move:
        return ADNobonus

    if opp_hit:
        return ADNobonus

    if MOVEtaunt in player_move:
        return ADsuper

    return ADadvantage
