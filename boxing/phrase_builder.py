from boxing_strings import *
import numpy as np

BIGHITS = ['argh', 'aooga', 'bada bing bada boom', 'bam', 'bang', 'batter up', 'bazinga', 'beep beep', 'boom', 'booya',
           'kaching', 'kerbam', 'choo choo', 'ding dong', 'dynomite', 'great scott', 'honk', 'knock knock', 'kerpow',
           'mamma mia', 'mazel tov', 'oof', 'pow', 'wham', 'whammo']
DOWNED = ['man overboard', 'ruh roh', 'splash']
TAUNTS = ['cock a doodle doo', 'neener neener', 'oh snap']
MISSES = ['bonjour', 'bon voyage', 'good grief', 'just kidding', 'whoops a daisy', 'wah wah', 'whoosh']


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
    third_line = "In the blue corner we have the challenger %s with their new coach. Siri was just telling me that this new coach yells out every single move to %s. Yep, that's right Siri, it is weird to see every jab, hook, and cross called out by a coach. %s relies on the coach to know when to protect their body or keep the hands up or even when to bob and weave. That's right Siri, this is a new era of boxing." % (blue, blue, blue_short)
    forth_line = "The fight is about to begin. Lets see what this new coach calls out first."
    return build_phrase([first_line, second_line, third_line, forth_line])

def build_midround(gs):
    pass


def build_betweenround(gs):
    pass


def build_gameover(gs):
    pass


def build_phrase(sentences):
    return '<speak>%s</speak>' % ' '.join(sentences)


def interjection(word):
    return '<say-as interpret-as="interjection">%s!</say-as>' % word


def rate(phrase, rate):
    return '<prosody rate="%d%%">%s</prosody>' % (rate, phrase)
