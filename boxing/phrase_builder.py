from boxing_strings import *
import numpy as np

BIGHITS = ['argh', 'aooga', 'bada bing bada boom', 'bam', 'bang', 'batter up', 'bazinga', 'beep beep', 'boom', 'booya',
           'kaching', 'kerbam', 'choo choo', 'ding dong', 'dynomite', 'great scott', 'honk', 'knock knock', 'kerpow',
           'mamma mia', 'mazel tov', 'oof', 'pow', 'wham', 'whammo']
DOWNED = ['man overboard', 'ruh roh', 'splash']
TAUNTS = ['cock a doodle doo', 'neener neener', 'oh snap', 'what a show stopping showboater']
MISSES = ['bon voyage', 'good grief', 'just kidding', 'whoops a daisy', 'wah wah', 'whoosh']
DANCEMOVES = ['did the moonwalk.', 'did the Hokey-Pokey.', 'did the Hustle.', 'did the charleston.', 'did the robot.',
              'did the twist.', 'did the <say-as interpret-as='"'spell-out'"'>YMCA.</say-as>', 'raised the roof.',
              'stuck out his chin.', 'blew a kiss.', 'curtsied.']


def build(gs):
    prompt = gs[ANNOUNCE]

    if ANNOUNCEIntro in prompt:
        return build_intro(gs)
    elif ANNOUNCEMidround in prompt:
        return build_midround(gs)
    elif ANNOUNCEBetweenRound in prompt:
        return build_betweenround(gs)
    else:
        return build_gameover(gs)


def name(gs, player=True, short=False):
    if player:
        n = gs[PLAYERNAME]
    else:
        n = gs[OPPONENTNAME]

    if not short:
        return n

    return np.random.choice(n.split(' '))


def build_intro(gs):
    blue = name(gs, player=True)
    blue_short = name(gs, player=True, short=True)
    red = name(gs, player=False)
    first_line = "This is Alexa for <say-as interpret-as='"'spell-out'"'>BHO</say-as> sports and I'm here with Siri at the south lake union boxing arena."
    second_line = "In the red corner we have the reigning champion %s." % red
    third_line = "In the blue corner we have the challenger %s with their new coach. Siri was just telling me that this new coach yells out every single move to %s. Yep, that's right Siri, it is weird to see every jab, hook, and cross called out by a coach. %s relies on the coach to know when to protect their body or keep the hands up or even when to bob and weave. That's right Siri, this is a new era of boxing." % (
        blue, blue, blue_short)
    forth_line = "The fight is about to begin. Lets see what this new coach calls out first."
    return build_phrase([first_line, second_line, third_line, forth_line])


def build_midround(gs):
    midround = []

    all_topics = sorted_named_topics(gs)
    for topic, name1, name2 in all_topics:
        phrase = ''
        if topic == TOPICShowboat:
            phrase = showboat_phrase(name1, name2)
        if topic == TOPICBlocked:
            phrase = blocked_phrase(name1, name2, gs)
        if topic == TOPICHit:
            phrase = hit_phrase(name1, name2, gs)
        if topic == TOPICHealthgood:
            phrase = healthgood_phrase(name1)
        if topic == TOPICHealthok:
            phrase = healthok_phrase(name1)
        if topic == TOPICHealthlow:
            phrase = healthlow_phrase(name1)
        if topic == TOPICStaminagood:
            phrase = staminagood_phrase(name1)
        if topic == TOPICStaminaok:
            phrase = staminaok_phrase(name1)
        if topic == TOPICStaminalow:
            phrase = staminalow_phrase(name1)
        if topic == TOPICBighit:
            phrase = bighit_phrase(name1, name2, gs)
        if topic == TOPICMiss:
            phrase = miss_phrase(name1, name2, gs)
        if topic == TOPICBoring:
            phrase = boring_phrase()
        if topic == TOPICHardtohit:
            phrase = hardtohit_phrase(name1, name2)

        if not phrase:
            phrase = notmuchhappening_phrase()
        midround.append(phrase)
    # IF THIS IS EMPTY DESCRIBE THE PUNCHES
    return ' '.join(midround)


def build_betweenround(gs):
    sc = score(gs)

    player_name = name(gs, player=True, short=True)
    op_name = name(gs, player=False, short=True)

    if sc[0] > sc[1]:
        leader = player_name
    else:
        leader = op_name

    round = gs[CURRENTROUND] - 1
    between1 = "And there's the bell. After %d rounds it looks like %s is ahead. It looks like this %s's coach is really helping. Here is the bell for the next round. What does %s's coach have in store next?" % (
        round, leader, player_name, player_name)
    return between1


def build_gameover(gs):
    player_name = name(gs, player=True, short=True)
    op_name = name(gs, player=False, short=True)

    player_hp = gs[PLAYERHP]
    op_hp = gs[OPPONENTHP]

    if op_hp <= 0:
        return knockout_phrase(player_name, op_name)

    if player_hp <= 0:
        return knockout_phrase(op_name, player_name)

    return decision_phrase(player_name, op_name, gs)


def decision_phrase(name1, name2, gs):
    sc = score(gs)
    print 'score %d - %d' % (sc[0], sc[1])
    rounds = gs[NUMROUNDS]

    winner = ''
    if sc[0] > sc[1]:
        winner = name1

    if sc[1] > sc[0]:
        winner = name2

    if winner == '':
        end1 = "And that's the final bell. After %d grueling rounds this match ends in a draw. It's all she wrote. Thanks for joining me and Siri here in south lake union. Please tune in next time." % rounds
    else:
        end1 = "And that's the final bell. After %d grueling rounds this match will be decided by the judges. And it's %s. %s wins the match. It's all she wrote. Thanks for joining me and Siri here in south lake union. Please tune in next time." % (
            rounds, winner, winner)

    return end1


def knockout_phrase(name1, name2):
    return "That's it. That's it. It's all over. %s just knocked out %s. It's all she wrote. Thanks for joining me and Siri here in south lake union. Please tune in next time." % (
        name1, name2)


def score(gs):
    player_history = gs[PLAYERHISTORY]
    op_history = gs[OPPONENTHISTORY]
    histories = [player_history, op_history]
    scores = [0, 0]
    for idx, history in enumerate(histories):
        sc = 0
        for move, did_hit in history:
            sc += score_move(move, did_hit)
        scores[idx] = sc
    return scores


def score_move(move, did_hit):
    if not did_hit:
        return 0

    if move == MOVEuppercut:
        return 3
    if move == MOVEcross or move == MOVEhook:
        return 2
    if move == MOVEjab:
        return 1
    return 0


def build_phrase(sentences):
    return '<speak>%s</speak>' % ' '.join(sentences)


def interjection(word):
    return '<say-as interpret-as="interjection">%s!</say-as>' % word


def rate(phrase, rate):
    return '<prosody rate="%d%%">%s</prosody>' % (rate, phrase)


def get_move_from_name(name, gs):
    if name in gs[PLAYERNAME]:
        move = gs[PLAYERMOVE]
    else:
        move = gs[OPPONENTMOVE]
    return move


def hit_phrase(name, opp_name, gs):
    move = get_move_from_name(name, gs)

    hit_phrase0 = '%s just smacked %s with a %s.' % (name, opp_name, move)
    hit_phrase1 = '%s lands a %s.' % (name, move)
    hit_phrase2 = 'A %s %s from %s finds the target.' % (adjective(), move, name)
    hit_phrase3 = '%s with a %s.' % (name, move)
    hit_phrase4 = 'A %s from %s.' % (move, name)
    hit_phrase5 = 'A %s to the %s from %s.' % (move, body_party(), name)
    hit_phrase6 = '%s with a %s %s.' % (name, hand(), move)
    hit_phrase7 = '%s with a %s %s.' % (name, adjective(), move)

    hit_phrases = [hit_phrase0, hit_phrase1, hit_phrase2, hit_phrase3, hit_phrase4, hit_phrase5, hit_phrase6,
                   hit_phrase7]
    return np.random.choice(hit_phrases)


def showboat_phrase(name, opp_name):
    if np.random.random() > 0.8:
        taunt = np.random.choice(TAUNTS)
        intrj = interjection(taunt)
    else:
        intrj = ''

    dance_move = name + ' just ' + np.random.choice(DANCEMOVES)
    first_line = ' '.join([intrj, dance_move])

    second1 = "I'm sure %s doesn't like being taunted." % opp_name
    second2 = ''
    second3 = 'You can see that %s is upset by the dance moves.' % opp_name
    second4 = '%s is really feeling it. Look out for a big one here.' % name
    second5 = 'That sure is intimidating.'
    second6 = 'I agree Siri, that would really piss me off.'
    second_line = np.random.choice([second1, second2, second3, second4, second5, second6])

    return ' '.join([first_line, second_line])


def healthgood_phrase(name1):
    health1 = '%s is looking better.' % name1
    health2 = 'Siri thinks %s is getting a second wind.' % name1
    return np.random.choice([health1, health2])


def healthok_phrase(name1):
    health1 = '%s is taking quite a few hits.' % name1
    health2 = '%s is getting roughed up.' % name1
    return np.random.choice([health1, health2])


def healthlow_phrase(name1):
    health1 = '%s is bleeding all over the place.' % name1
    health2 = 'Can %s even see? Their eyes are almost swollen shut.' % name1
    health3 = '%s looks really rough.' % name1
    return np.random.choice([health1, health2, health3])


def staminagood_phrase(name1):
    stamina1 = '%s looks fresh.' % name1
    stamina2 = "%s's preparation is really showing. %s looks very strong out there." % (name1, name1)
    return np.random.choice([stamina1, stamina2])


def staminaok_phrase(name1):
    stamina1 = '%s is starting to slow down a bit.' % name1
    stamina2 = '%s is getting fatigued. All these big punches are starting to wear them down.' % name1
    return np.random.choice([stamina1, stamina2])


def staminalow_phrase(name1):
    stamina1 = '%s is dead tired.' % name1
    stamina2 = '%s has nothing left in the tank.' % name1
    stamina3 = "I'm not sure %s has enough energy to even throw a punch right now." % name1
    return np.random.choice([stamina1, stamina2, stamina3])


def boring_phrase():
    boring1 = 'Yawn. It has been a while since we have seen some action eh Siri?'
    boring2 = 'What a slow fight!'
    boring3 = 'The ref just stepped in to tell the boxers to get to work here.'
    boring4 = 'The match is so slow some of the crowd is leaving.'
    boring5 = 'What a sleeper. Someone needs to throw a punch.'
    return np.random.choice([boring1, boring2, boring3, boring4, boring5])


def sorted_by_exciting(topics):
    # ordered highest excitement to lowest
    most_exciting_topics = [TOPICBighit, TOPICShowboat, TOPICHardtohit, TOPICHealthlow, TOPICStaminalow, TOPICHit,
                            TOPICBlocked, TOPICMiss]

    # push to the front from least to most exciting
    for exciting_topic in reversed(most_exciting_topics):
        for idx in range(len(topics)):
            topic, name1, name2 = topics[idx]
            if topic == exciting_topic:
                exciting = topics.pop(idx)
                topics.insert(0, exciting)

    return topics


def sorted_named_topics(gs):
    player_name = name(gs, player=True, short=True)
    opp_name = name(gs, player=False, short=True)

    player_topics, opp_topics = gs[TOPICS]

    player_topics_named = [(topic, player_name, opp_name) for topic in player_topics]
    opp_topics_named = [(topic, opp_name, player_name) for topic in opp_topics]
    all_topics = player_topics_named + opp_topics_named
    sorted_topics = sorted_by_exciting(all_topics)
    return sorted_topics


def bighit_phrase(name1, name2, gs):
    move = get_move_from_name(name1, gs)

    if np.random.random() > 0.4:
        hit = np.random.choice(BIGHITS)
        intrj = interjection(hit)
    else:
        intrj = ''

    bighit1 = '%s just laid down the law on %s with a big %s.' % (name1, name2, move)
    bighit2 = "%s's parents can feel that %s." % (name2, move)
    bighit3 = 'A big %s from %s will likely send %s to the <say-as interpret-as='"'spell-out'"'>CTE</say-as> protocol tomorrow.' % (
        move, name1, name2)
    bighit4 = 'Aw lawdy lawdy what a big %s from %s.' % (move, name1)

    bighit = np.random.choice([bighit1, bighit2, bighit3, bighit4])
    return ' '.join([intrj, bighit])


def miss_phrase(name1, name2, gs):
    move = get_move_from_name(name1, gs)

    miss1 = 'A big whiff from %s.' % name1
    miss2 = '%s %s that %s from %s.' % (name2, dodge(), move, name1)
    miss3 = 'No chance that %s from %s was landing.' % (move, name1)
    miss4 = '%s misses with a %s.' % (name1, move)
    miss5 = '%s misses the %s.' % (name1, move)
    miss6 = '%s makes em miss.' % name2
    miss7 = 'That %s from %s was way off.' % (move, name1)
    return np.random.choice([miss1, miss2, miss3, miss4, miss5, miss6, miss7])


def hardtohit_phrase(name1, name2):
    miss1 = "%s can't hit a thing." % name1
    miss2 = 'Can %s even see %s?' % (name1, name2)
    miss3 = '%s just keeps missing.' % (name1)
    miss4 = '%s is impossible to hit.' % (name2)
    return np.random.choice([miss1, miss2, miss3, miss4])

def blocked_phrase(name1, name2, gs):
    move = get_move_from_name(name1, gs)
    block = get_move_from_name(name2, gs)
    block1 = '%s telegraphed that %s. %s easily blocks it.' % (name1, move, name2)
    block2 = '%s blocks a %s from %s.' % (name2, move, name1)
    block3 = 'It will take more than that %s from %s.' % (move, name1)
    block4 = "%s's %s defense is really good right now." % (name2, block)
    block5 = '%s from %s.' % (block, name2)
    return np.random.choice([block1, block2, block3, block4, block5])

def notmuchhappening_phrase():
    notmuch1 = 'Not a lot happening right now'
    notmuch2 = 'Siri wake up - something might happen'
    notmuch3 = 'Not a lot of action right now'
    notmuch4 = 'The ref is asking the boxers to get to work'
    return np.random.choice([notmuch1, notmuch2, notmuch3, notmuch4])


def body_party():
    return np.random.choice(['head', 'mouth', 'body', 'face', 'ear', 'chin'])


def hand():
    return np.random.choice(['left', 'right'])


def adjective():
    return np.random.choice(['speedy', 'quick', 'heavy', 'slow', 'crafty'])


def dodge():
    return np.random.choice(['avoided', 'side stepped', 'got out of the way of', 'ducked'])
