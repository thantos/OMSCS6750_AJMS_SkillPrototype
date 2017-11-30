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
PLAYERHISTORY = 'player history'


def add_dict_to_session(d, session):
    for key in d:
        val = d[key]
        session[key] = val
    return session


class TestBoxingSkillAdaptor(TestCase):
    def test_player_wins(self):

        unfair_session = {OPPONENTMOVE: MOVEuppercut, PLAYERBONUS: ADsuper, OPPONENTBONUS: ADexhausted}
        session = BoxingSkillAdaptor().on_intent({INTENTName: INTENTSelect}, None)[SESSION]
        for i in range(100):

            session = BoxingSkillAdaptor().on_intent({INTENTName: INTENTPunch}, session)[SESSION]
            meta = session['meta']

            # give the player an advantage every round
            meta = add_dict_to_session(unfair_session, meta)

            if meta[ANNOUNCE] == ANNOUNCEGameOver:
                break

            session['meta'] = meta

        self.assertTrue(meta[OPPONENTHP] <= 20)

    def test_draw(self):

        player_move = {OPPONENTMOVE: MOVEprotect}

        session = BoxingSkillAdaptor().on_intent({INTENTName: INTENTSelect}, None)[SESSION]
        session[OPPONENTMOVE] = MOVEprotect

        for i in range(100):
            session = BoxingSkillAdaptor().on_intent({INTENTName:INTENTPunch}, session)[SESSION]
            meta = session['meta']

            # give the player an advantage every round
            meta = add_dict_to_session(player_move, meta)

            if meta[ANNOUNCE] == ANNOUNCEGameOver:
                break

            session['meta'] = meta
        self.assertTrue(i < 99)


    def test_load_game(self):

        response = BoxingSkillAdaptor().on_intent({'name': 'sceneSelectIntent'}, None)

        meta = response[SESSION]['meta']
        self.assertEqual(meta['announce'], 'mid round')



    def test_first_turn_loads(self):

        session = BoxingSkillAdaptor().on_intent({INTENTName: INTENTSelect}, None)[SESSION]
        meta = session['meta']
        self.assertEqual(len(meta[PLAYERHISTORY]), 0)