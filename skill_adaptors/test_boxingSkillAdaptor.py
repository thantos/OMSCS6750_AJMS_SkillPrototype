from unittest import TestCase
from boxing_skill_adaptor import *

INTENTName = 'name'
INTENTPunch = 'punchIntent'
ANNOUNCE = 'announce'
MOVEuppercut = 'uppercut'
OPPONENTHP = 'opponent hp'
PLAYERMOVE = 'player move'
OPPONENTMOVE = 'opponent move'
PLAYERBONUS = 'player bonus'
OPPONENTBONUS = 'opponent bonus'
ADsuper = 'super'
ADexhausted = 'exhausted'
SESSION = 'sessionAttributes'
MOVEprotect = 'protects the body'
ANNOUNCEGameOver = 'game over'
INTENTSelect = 'sceneSelectIntent'

def add_dict_to_session(d, session):
    for key in d:
        val = d[key]
        session[key] = val
    return session


class TestBoxingSkillAdaptor(TestCase):
    def test_player_wins(self):
        uppercut_intent = {INTENTName: INTENTPunch}
        unfair_session = {OPPONENTMOVE: MOVEuppercut, PLAYERBONUS: ADsuper, OPPONENTBONUS: ADexhausted}

        session = BoxingSkillAdaptor().on_intent({INTENTName:INTENTSelect}, None)[SESSION]
        for i in range(10):

            session = BoxingSkillAdaptor().on_intent({INTENTName:INTENTPunch}, session)[SESSION]

            # give the player an advantage every round
            session = add_dict_to_session(unfair_session, session)

            if session[ANNOUNCE] == ANNOUNCEGameOver:
                break

        self.assertTrue(session[OPPONENTHP] <= 0)

    def test_draw(self):
        uppercut_intent = {INTENTName: MOVEprotect}
        player_move = {OPPONENTMOVE: MOVEprotect}

        session = BoxingSkillAdaptor().on_intent({INTENTName:INTENTSelect}, None)[SESSION]
        session[OPPONENTMOVE] = MOVEprotect
        for i in range(10):

            session = BoxingSkillAdaptor().on_intent({INTENTName:INTENTPunch}, session)[SESSION]

            # give the player an advantage every round
            session = add_dict_to_session(player_move, session)

            if session[ANNOUNCE] == ANNOUNCEGameOver:
                break

    def test_load_game(self):

        response = BoxingSkillAdaptor().on_intent({'name':'sceneSelectIntent'}, None)
        first_round_speech = response['response']['outputSpeech']['ssml']
        self.assertTrue('This is Alexa' in first_round_speech)