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

intents = ['uppercutIntent', 'jabIntent', 'blockpunchIntent', 'footworkIntent', 'crossIntent', 'hookIntent',
           'bobIntent', 'tauntIntent', 'protectbodyIntent', 'handsupIntent', 'feintIntent']


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
            session = BoxingSkillAdaptor().on_intent({INTENTName: INTENTPunch}, session)[SESSION]
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

    def test_before_announces_bell_after_action(self):
        session = BoxingSkillAdaptor().on_intent({INTENTName: INTENTSelect}, None)[SESSION]
        meta = session['meta']
        meta['turns'] = [2, 2, 2]
        session['meta'] = meta

        session = BoxingSkillAdaptor().on_intent({INTENTName: 'uppercutIntent'}, session)[SESSION]

        session = BoxingSkillAdaptor().on_intent({INTENTName: 'uppercutIntent'}, session)[SESSION]

        # requires inpection - should end with the mid round text
        self.assertTrue('bell' in session['meta']['speech'])

    def test_random_game(self):
        session = BoxingSkillAdaptor().on_intent({INTENTName: INTENTSelect}, None)[SESSION]
        meta = session['meta']
        meta['player bonus'] = 'super'
        session['meta'] = meta
        for _ in range(2):
            for i in range(10):
                meta = session['meta']

                # if len(meta['player history']) > 0:
                #     print meta['player history'][-1],  meta['player bonus'], meta['opponent history'][-1], meta['opponent bonus']
                # print meta['speech']
                # print

                session = BoxingSkillAdaptor().on_intent({INTENTName: 'jabIntent'}, session)[SESSION]
                if session['meta']['announce'] == 'game over':
                    break

                    # meta = session['meta']
                    # print meta['speech']
