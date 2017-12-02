from boxing_strings import *


# return two lists - one for player one for opp
def topics(game_state_prev, game_state):
    player_health = health_topic(game_state_prev, game_state, True)
    player_stamina = stamina_topic(game_state_prev, game_state, True)
    player_hits = hit_topic(game_state, True)
    player_topics = player_health + player_stamina + player_hits

    op_health = health_topic(game_state_prev, game_state, False)
    op_stamina = stamina_topic(game_state_prev, game_state, False)
    op_hits = hit_topic(game_state, False)
    op_topics = op_health + op_stamina + op_hits

    game_state[TOPICS] = [player_topics, op_topics]
    return game_state


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


def health(gamestate, player=True):
    if player:
        hp = gamestate[PLAYERHP]
    else:
        hp = gamestate[OPPONENTHP]

    health = TOPICHealthgood

    max_health = 20
    if hp < (0.33 * max_health):
        health = TOPICHealthlow
    elif hp < (0.66 * max_health):
        health = TOPICHealthok

    return health


# only add a topic if this changed
def health_topic(game_state_prev, game_state, player=True):
    prev_health = health(game_state_prev, player)
    cur_health = health(game_state, player)

    topic = []
    if prev_health != cur_health:
        topic = [cur_health]

    return topic


def stamina(gamestate, player=True):
    if player:
        st = gamestate[PLAYERSTAMINA]
    else:
        st = gamestate[OPPONENTSTAMINA]

    stamina = TOPICStaminagood

    max_stamina = 10
    if st < 0.33 * max_stamina:
        stamina = TOPICStaminalow
    elif st < 0.66 * max_stamina:
        stamina = TOPICStaminaok

    return stamina


# only add a topic if this changed
def stamina_topic(game_state_prev, game_state, player=True):
    prev_stamina = stamina(game_state_prev, player)
    cur_stamina = stamina(game_state, player)

    topic = []
    if prev_stamina != cur_stamina:
        topic = [cur_stamina]

    return topic


def hit_topic(game_state, player=True):
    if player:
        history = game_state[PLAYERHISTORY]
        op_history = game_state[OPPONENTHISTORY]
    else:
        history = game_state[OPPONENTHISTORY]
        op_history = game_state[PLAYERHISTORY]

    topics = []

    if blocked(history, op_history):
        topics.append(TOPICBlocked)
    if wrapped_up(op_history):
        topics.append(TOPICWrapup)

    if missed(history) and not blocked(history, op_history):
        topics.append(TOPICMiss)
    elif big_hit(history) and not missed(history):
        topics.append(TOPICBighit)

    elif hard_to_hit(op_history):
        topics.append(TOPICHardtohit)

    elif showboating(history, op_history):
        topics.append(TOPICShowboat)
    elif regular_hit(history):
        topics.append(TOPICHit)
    elif both_block(history, op_history) and player:
        topics.append(TOPICBothblock)

    return topics


def both_block(history, op_history):
    current_move, current_did_hit = history[-1]
    op_current_move, op_current_did_hit = op_history[-1]
    return block_move(current_move) and block_move(op_current_move)


def missed(history):
    current_move, current_did_hit = history[-1]
    return not current_did_hit and attack_move(current_move)


def big_hit(history):
    current_move, current_did_hit = history[-1]
    if current_move == MOVEuppercut:
        return True
    return False


def regular_hit(history):
    current_move, current_did_hit = history[-1]
    if attack_move(current_move) and current_did_hit:
        return True
    return False


def hard_to_hit(op_history):
    recent_history = op_history[-3:]

    if len(recent_history) < 3:
        return False

    # if the last three op moves were misses -> player is hard to hit
    for move, hit in recent_history:
        if not hit and attack_move(move):
            continue
        return False
    return True


def showboating(history, op_history):
    current_move, current_did_hit = history[-1]
    op_current_move, op_current_did_hit = op_history[-1]

    op_landed_hit = op_current_did_hit and attack_move(op_current_move)
    if current_move == MOVEtaunt and not op_landed_hit:
        return True
    return False


def blocked(history, op_history):
    if missed(history):
        op_current_move, op_current_did_hit = op_history[-1]
        if block_move(op_current_move):
            return True
    return False


def wrapped_up(op_history):
    op_current_move, op_current_did_hit = op_history[-1]
    return op_current_move == MOVEwrapup and op_current_did_hit


def attack_move(move):
    return move in [MOVEuppercut, MOVEjab, MOVEcross, MOVEhook]


def block_move(move):
    return move in [MOVEhandsup, MOVEprotect, MOVEbob, MOVEfootwork]
