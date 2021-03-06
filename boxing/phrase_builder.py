from boxing_strings import *
from random import choice, random

BIGHITS = ['argh', 'aooga', 'bada bing bada boom', 'bam', 'bang', 'batter up', 'bazinga', 'beep beep', 'boom', 'booya',
           'kaching', 'kerbam', 'choo choo', 'ding dong', 'dynomite', 'honk', 'knock knock', 'kerpow',
           'mamma mia', 'mazel tov', 'oof', 'pow', 'wham', 'whammo']
DOWNED = ['man overboard', 'ruh roh', 'splash']
TAUNTS = ['cock a doodle doo', 'neener neener', 'oh snap', 'what a showboat']
MISSES = ['bon voyage', 'good grief', 'just kidding', 'whoops a daisy', 'wah wah', 'whoosh']
DANCEMOVES = ['did the moonwalk.', 'did the Hokey-Pokey.', 'did the Hustle.', 'did the charleston.', 'did the robot.',
              'did the twist.', 'did the <say-as interpret-as='"'spell-out'"'>YMCA.</say-as>', 'raised the roof.',
              'stuck out his chin.', 'blew a kiss.', 'curtsied.']


def reprompt(gs):
    player_name = name(gs, player=True, short=True)
    reprompt1 = '%s looks to the corner for help.' % player_name
    reprompt2 = '%s is waiting for the coach to say something.' % player_name
    reprompt3 = 'What will the coach call out next, Siri?'
    return build_phrase(choice([reprompt1, reprompt2, reprompt3]))


def build(gs):
    prompt = gs[ANNOUNCE]

    if ANNOUNCEIntro in prompt:
        phrase = build_intro(gs)
        gs[ANNOUNCE] = ANNOUNCEMidround
    elif ANNOUNCEMidround in prompt:
        phrase = build_midround(gs)
        phrase += " " + coach_phrase(gs)
    elif ANNOUNCEBetweenRound in prompt:
        phrase = build_midround(gs)
        phrase += " " + build_betweenround(gs)
        gs[ANNOUNCE] = ANNOUNCEMidround
    else:
        phrase = build_midround(gs)
        phrase += " " + build_gameover(gs)

    return build_phrase(phrase)


def name(gs, player=True, short=False):
    if player:
        n = gs[PLAYERNAME]
    else:
        n = gs[OPPONENTNAME]

    if not short:
        return n

    return choice(n.split(' '))


def build_intro(gs):
    blue = name(gs, player=True)
    blue_short = name(gs, player=True, short=True)
    red = name(gs, player=False)
    first_line = "This is Alexa for <say-as interpret-as='"'spell-out'"'>BHO</say-as> sports and I'm here with Siri at the south lake union boxing arena."
    second_line = "In the red corner we have the reigning champion %s." % red
    third_line = "In the blue corner we have the challenger %s with his new coach. Siri was just telling me that this new coach yells out every single move to %s. Yep, that's right Siri, it is weird to see every jab, hook, and cross called out by a coach. %s relies on the coach to know when to protect his body or keep his hands up or even when to bob and weave. That's right Siri, this is a new era of boxing." % (
        blue, blue, blue_short)
    forth_line = "The fight is about to begin. Lets see what this new coach calls out first."
    return ' '.join([first_line, second_line, third_line, forth_line])


def build_midround(gs):
    midround = []

    all_topics = sorted_named_topics(gs)
    for topic, name1, name2 in all_topics:
        phrase = ''
        if topic == TOPICShowboat:
            phrase = showboat_phrase(name1, name2)
        elif topic == TOPICBlocked:
            phrase = blocked_phrase(name1, name2, gs)
        elif topic == TOPICHit:
            phrase = hit_phrase(name1, name2, gs)
        elif topic == TOPICHealthgood:
            phrase = healthgood_phrase(name1)
        elif topic == TOPICHealthok:
            phrase = healthok_phrase(name1)
        elif topic == TOPICHealthlow:
            phrase = healthlow_phrase(name1)
        elif topic == TOPICStaminagood:
            phrase = staminagood_phrase(name1)
        elif topic == TOPICStaminaok:
            phrase = staminaok_phrase(name1)
        elif topic == TOPICStaminalow:
            phrase = staminalow_phrase(name1)
        elif topic == TOPICBighit:
            phrase = bighit_phrase(name1, name2, gs)
        elif topic == TOPICMiss:
            phrase = miss_phrase(name1, name2, gs)
        elif topic == TOPICBoring:
            phrase = boring_phrase()
        elif topic == TOPICHardtohit:
            phrase = hardtohit_phrase(name1, name2)
        elif topic == TOPICWrapup:
            phrase = wrapup_phrase(name1, name2)
        elif topic == TOPICBothblock:
            phrase = bothblock_phrase(name1, name2)
        elif topic == TOPICHeatingup:
            phrase = heatingup_phrase(name1)
        elif topic == TOPICFire:
            phrase = onfire_phrase(name1)

        midround.append(phrase)
    if len(midround) == 0:
        midround = [notmuchhappening_phrase()]

    # Need to add topics for wrapup, feint and both block
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
    player_score, op_score = score(gs)

    rounds = gs[NUMROUNDS]

    winner = ''
    if player_score > op_score:
        winner = name1
    if op_score > player_score:
        winner = name2

    if winner == '':
        end1 = "And that's the final bell. After %d grueling rounds this match ends in a draw. That iss all she wrote. Thanks for joining me and Siri here in south lake union. Please tune in next time." % rounds
    else:
        end1 = "And that's the final bell. After %d grueling rounds this match will be decided by the judges. By a score of %d to %d... %s wins the match. That is all she wrote. Thanks for joining me and Siri here in south lake union. Please tune in next time." % (
            rounds, player_score, op_score, winner)

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


def build_phrase(phrase):
    return '%s' % phrase


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
    return choice(hit_phrases)


def showboat_phrase(name, opp_name):
    if random() > 0.4:
        taunt = choice(TAUNTS)
        intrj = interjection(taunt)
    else:
        intrj = ''

    dance_move = name + ' just ' + choice(DANCEMOVES) + " to taunt %s." % opp_name
    first_line = ' '.join([intrj, dance_move])

    second1 = "I'm sure %s doesn't like being taunted." % opp_name
    second2 = ''
    second3 = 'You can see that %s is upset by the dance moves.' % opp_name
    second4 = '%s is really feeling it. Look out for a big one here.' % name
    second5 = 'That sure is intimidating.'
    second6 = 'I agree Siri, that would really piss me off.'
    second_line = choice([second1, second2, second3, second4, second5, second6])

    return ' '.join([first_line, second_line])


def healthgood_phrase(name1):
    health1 = '%s is looking better.' % name1
    health2 = 'Siri thinks %s is getting a second wind.' % name1
    return choice([health1, health2])


def healthok_phrase(name1):
    health1 = '%s is taking quite a few hits.' % name1
    health2 = '%s is getting roughed up.' % name1

    health = choice([health1, health2])
    increase = how_to_increase_health(name1)
    return " ".join([health, increase])


def healthlow_phrase(name1):
    health1 = '%s is bleeding all over the place.' % name1
    health2 = 'Can %s even see? His eyes are almost swollen shut.' % name1
    health3 = '%s looks really rough.' % name1

    health = choice([health1, health2, health3])
    increase = how_to_increase_health(name1)
    return " ".join([health, increase])


def staminagood_phrase(name1):
    stamina1 = '%s looks fresh.' % name1
    stamina2 = "%s's preparation is really showing." % name1
    stamina3 = "%s looks very strong out there" % name1
    return choice([stamina1, stamina2, stamina3])


def staminaok_phrase(name1):
    stamina1 = '%s is starting to slow down a bit.' % name1
    stamina2 = '%s is getting fatigued.' % name1
    stamina3 = '%s is losing stamina.' % name1

    stamina = choice([stamina1, stamina2, stamina3])
    increase = how_to_increase_health(name1)
    return " ".join([stamina, increase])


def staminalow_phrase(name1):
    stamina1 = '%s is dead tired.' % name1
    stamina2 = '%s has nothing left in the tank.' % name1
    stamina3 = "Does %s hav enough energy to even throw a punch right now?" % name1

    stamina = choice([stamina1, stamina2, stamina3])
    increase = how_to_increase_health(name1)
    return " ".join([stamina, increase])


def how_to_increase_stamina(name1):
    increase_stamina1 = '%s should keep his hands up to regain energy.' % name1
    increase_stamina2 = '%s should protect his body to stop these blows.' % name1
    increase_stamina3 = '%s should try to wrap him up to rest a bit.' % name1
    return choice([increase_stamina1, increase_stamina2, increase_stamina3])


def how_to_increase_health(name1):
    increase_health1 = '%s needs to move around.' % name1
    increase_health2 = '%s needs to work on his footwork.' % name1
    increase_health3 = '%s should try to bob and weave.' % name1
    return choice([increase_health1, increase_health2, increase_health3])


1


def boring_phrase():
    boring1 = 'Yawn. It has been a while since we have seen some action eh Siri?'
    boring2 = 'What a slow fight!'
    boring3 = 'The ref just stepped in to tell the boxers to get to work here.'
    boring4 = 'The match is so slow some of the crowd is leaving.'
    boring5 = 'What a sleeper. Someone needs to throw a punch.'
    boring6 = "They're off like a herd of turtles!"
    return choice([boring1, boring2, boring3, boring4, boring5, boring6])


def sorted_by_exciting(topics):
    # ordered highest excitement to lowest
    most_exciting_topics = [TOPICBighit, TOPICShowboat, TOPICHit, TOPICFire, TOPICHeatingup,  TOPICHardtohit, TOPICHealthlow, TOPICStaminalow,
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
    intrj = interjection(choice(BIGHITS))
    hit = hit_phrase(name1, name2, gs)
    return ' '.join([intrj, hit])


def miss_phrase(name1, name2, gs):
    move = get_move_from_name(name1, gs)

    miss1 = 'A big whiff from %s.' % name1
    miss2 = '%s %s that %s from %s.' % (name2, dodge(), move, name1)
    miss3 = 'No chance that %s from %s was landing.' % (move, name1)
    miss4 = '%s misses with a %s.' % (name1, move)
    miss5 = '%s misses the %s.' % (name1, move)
    miss6 = '%s gets out of the way of that %s from %s.' % (name2, move, name1)
    miss7 = 'That %s from %s was way off.' % (move, name1)
    return choice([miss1, miss2, miss3, miss4, miss5, miss6, miss7])


def hardtohit_phrase(name1, name2):
    miss1 = "%s can't hit a thing." % name1
    miss2 = 'Can %s even see %s?' % (name1, name2)
    miss3 = '%s just keeps missing.' % (name1)
    miss4 = '%s is impossible to hit.' % (name2)
    return choice([miss1, miss2, miss3, miss4])


def blocked_phrase(name1, name2, gs):
    move = get_move_from_name(name1, gs)
    block = get_move_from_name(name2, gs)
    block1 = '%s telegraphed that %s. %s easily blocks it.' % (name1, move, name2)
    block2 = '%s blocks a %s from %s.' % (name2, move, name1)
    block3 = 'It will take more than that %s from %s to hit %s.' % (move, name1, name2)
    block4 = "%s's %s defense is really good right now." % (name2, block)
    return choice([block1, block2, block3, block4])


def notmuchhappening_phrase():
    notmuch1 = 'Not a lot happening right now.'
    notmuch2 = 'Siri wake up - something might happen.'
    notmuch3 = 'Not a lot of action right now.'
    notmuch4 = 'The ref is asking the boxers to get to work.'
    notmuch5 = 'The ref is separating the two fighters.'
    notmuch6 = 'These guys are looking for an opening.'
    notmuch7 = 'There is a lot of dancing around going on.'

    return choice([notmuch1, notmuch2, notmuch3, notmuch4, notmuch5, notmuch6, notmuch7])


def coach_phrase(gs):
    name1 = name(gs, player=True, short=True)
    coach1 = '%s looks to his coach for help.' % name1
    coach2 = '%s asks his coach for help.' % name1
    coach3 = '%s is looking for help from the corner.' % name1
    coach4 = "%s can't hear his coach." % name1
    coach5 = "%s is waiting for his coach to help." % name1
    coach6 = "What will %s's coach call out next?" % name1
    coach7 = "What is on %s's coach's mind?" % name1
    return choice([coach1, coach2, coach3, coach4, coach5, coach6, coach7])


def wrapup_phrase(name1, name2):
    wrap1 = '%s wraps up %s.' % (name2, name1)
    wrap2 = '%s grabs at %s and wraps him up.' % (name2, name1)
    wrap3 = '%s gets %s up on the ropes.' % (name2, name1)
    wrap4 = '%s is wrapped up by %s.' % (name1, name2)
    return choice([wrap1, wrap2, wrap3, wrap4])


def bothblock_phrase(name1, name2):
    block1 = 'These fighters are playing it safe.'
    block2 = 'Both fighters are scared to throw punches.'
    block3 = 'It looks like both fighters are defensive.'
    block4 = 'It looks like a block party out there. Everyone is putting up blocks but no punches.'
    return choice([block1, block2, block3, block4])


def heatingup_phrase(name1):
    heating1 = '%s is heating up.' % name1
    heating2 = 'Lookout Siri, %s is heating up.' % name1
    return choice([heating1, heating2])

def onfire_phrase(name1):
    onfire1 = '%s is on fire!' % name1
    onfire2 = 'Whoa! %s is buring up!' % name1
    onfire3 = '%s is super hot!' % name1
    onfire4 = "%s can't miss!" % name1
    return choice([onfire1, onfire2, onfire3, onfire4])



def body_party():
    return choice(['head', 'mouth', 'body', 'face', 'ear', 'chin'])


def hand():
    return choice(['left', 'right'])


def adjective():
    return choice(['speedy', 'quick', 'heavy', 'slow', 'crafty'])


def dodge():
    return choice(['avoided', 'side stepped', 'got out of the way of', 'ducked'])
