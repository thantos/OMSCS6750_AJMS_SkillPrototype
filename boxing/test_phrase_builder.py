from unittest import TestCase

from match import *
from boxing_strings import *
from modifiers import *
from boxer import *
from phrase_builder import *


class TestMoves(TestCase):
    def setUp(self):
        self.attack_moves = [MOVEcross, MOVEhook, MOVEjab, MOVEuppercut]
        self.defense_moves = [MOVEbob, MOVEfootwork, MOVEhandsup, MOVEprotect]
        self.moves = [MOVEjab, MOVEcross, MOVEhook, MOVEuppercut, MOVEwrapup, MOVEfeint, MOVEtaunt, MOVEbob,
                      MOVEfootwork, MOVEhandsup, MOVEprotect]

    # what Alexa will say
    def test_alexa_intro(self):
        gs = initialize({PLAYERMOVE: MOVEtaunt})
        phrase = build(gs)
        self.assertTrue(phrase)

    def test_alexa_midround(self):
        gs = initialize({PLAYERMOVE: MOVEtaunt})
        gs[PLAYERBONUS] = ADsuper
        gs[OPPONENTMOVE] = MOVEhandsup

        gs = update(gs)

        phrase = build(gs)
        self.assertTrue(phrase)
