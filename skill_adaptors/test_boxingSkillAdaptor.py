from unittest import TestCase
from boxing_skill_adaptor import *
from boxing_strings import *


def add_dict_to_session(d, session):
    for key in d:
        val = d[key]
        session[key] = val
    return session


class TestBoxingSkillAdaptor(TestCase):
    def test_player_wins(self):
        uppercut_intent = {INTENTName: MOVEuppercut}
        unfair_session = {OPPONENTMOVE: MOVEuppercut, PLAYERBONUS: ADsuper, OPPONENTBONUS: ADexhausted}

        session = dict(unfair_session)
        for i in range(10):

            session = BoxingSkillAdaptor().on_intent(uppercut_intent, session)[SESSION]

            # give the player an advantage every round
            session = add_dict_to_session(unfair_session, session)

            if session[ANNOUNCE] == ANNOUNCEGameOver:
                break

        self.assertTrue(session[OPPONENTHP] <= 0)

    def test_draw(self):
        uppercut_intent = {INTENTName: MOVEprotect}
        player_move = {OPPONENTMOVE: MOVEprotect}

        session = dict(player_move)
        for i in range(10):

            session = BoxingSkillAdaptor().on_intent(uppercut_intent, session)[SESSION]

            # give the player an advantage every round
            session = add_dict_to_session(player_move, session)

            if session[ANNOUNCE] == ANNOUNCEGameOver:
                break

        self.assertTrue(session[OPPONENTHP] == session[PLAYERHP])
        self.assertTrue(session[OPPONENTHP] == 20)
