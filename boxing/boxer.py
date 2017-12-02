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
        history = game_state[PLAYERHISTORY]
        op_history = game_state[OPPONENTHISTORY]
    else:
        history = game_state[OPPONENTHISTORY]
        op_history = game_state[PLAYERHISTORY]

    player_move, player_hit = history[-1]
    opp_move, opp_hit = op_history[-1]

    if on_fire(history):
        return ADOnfire

    if heating_up(history):
        return ADadvantage

    if MOVEuppercut in player_move and player_hit:
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


# heating up when the last two punches land
def heating_up(history):
    if len(history) < 2:
        return False

    move, hit = history[-1]
    prev_move, prev_hit = history[-2]

    two_attacks = attack_move(move) and attack_move(prev_move)
    two_hits = hit and prev_hit
    return two_attacks and two_hits


def on_fire(history):
    if len(history) < 3:
        return False

    move, hit = history[-1]
    prev_move, prev_hit = history[-2]
    prev_prev_move, prev_prev_hit = history[-3]
    three_attacks = attack_move(move) and attack_move(prev_move) and attack_move(prev_prev_move)
    three_hits = hit and prev_hit and prev_prev_hit
    return three_attacks and three_hits


def attack_move(move):
    return move in [MOVEjab, MOVEuppercut, MOVEcross, MOVEhook]
