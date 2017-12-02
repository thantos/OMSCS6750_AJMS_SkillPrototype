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
    if has_super(bonus) or has_onfire(bonus):
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


def has_onfire(bonus):
    return ADOnfire in bonus


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
        prev_bonus = game_state[PLAYERBONUS]
    else:
        history = game_state[OPPONENTHISTORY]
        op_history = game_state[PLAYERHISTORY]
        prev_bonus = game_state[OPPONENTBONUS]

    player_move, player_hit = history[-1]
    opp_move, opp_hit = op_history[-1]

    if on_fire(history, op_history, prev_bonus):
        return ADOnfire

    if heating_up(history, op_history):
        return ADadvantage

    if blocked_op(history, op_history):
        return ADadvantage

    if MOVEuppercut in player_move and player_hit:
        return ADdisadvantage

    if MOVEhook in player_move:
        return ADNobonus

    if MOVEcross in player_move:
        return ADNobonus

    if MOVEjab in player_move:
        return ADNobonus

    if MOVEwrapup in player_move and not attack_move_hit(op_history, 1):
        return ADadvantage

    if opp_hit:
        return ADNobonus

    if MOVEtaunt in player_move:
        return ADsuper

    return ADNobonus


def blocked_op(history, op_history):
    player_move, player_hit = history[-1]
    op_move, op_hit = op_history[-1]

    op_missed_attack = attack_move(op_move) and not op_hit
    player_blocked = defense_move(player_move)
    return op_missed_attack and player_blocked


def attack_move_hit(history, index):
    move, hit = history[-index]
    return attack_move(move) and hit


def last_two_hit(history):
    return attack_move_hit(history, 1) and attack_move_hit(history, 2)


def last_three_hit(history):
    return last_two_hit(history) and attack_move_hit(history, 3)


def successful_attack(history, last_n_turns):
    for n in range(last_n_turns):
        if attack_move_hit(history, n + 1):
            return True
    return False


# heating up when the last two punches land
def heating_up(history, op_history):
    if len(history) < 2:
        return False

    return last_two_hit(history) and not successful_attack(op_history, 2)


def on_fire(history, op_history, prev_bonus):
    if len(history) < 3:
        return False

    # only cool down once you get hit
    if prev_bonus and not attack_move_hit(op_history, 1):
        return True

    return last_three_hit(history) and not successful_attack(op_history, 3)


def attack_move(move):
    return move in [MOVEjab, MOVEuppercut, MOVEcross, MOVEhook]


def defense_move(move):
    return move in [MOVEhandsup, MOVEbob, MOVEfootwork, MOVEprotect]
