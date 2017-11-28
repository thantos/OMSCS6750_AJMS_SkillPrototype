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

    def test_alexa_midround(self):
        gs = initialize({PLAYERMOVE: MOVEuppercut})
        gs[OPPONENTMOVE] = MOVEuppercut
        gs[PLAYERBONUS] = ADsuper

        for i in range(500):
            gs[OPPONENTMOVE] = MOVEbob
            gs[PLAYERMOVE] = MOVEjab
            gs = update(gs)

            phrase = build(gs)
            print gs[CURRENTTURN], gs[CURRENTROUND], phrase
            # run this a bunch with random moves and find all the mistackes
            # A big Lincoln from George will likely send uppercut to the <say-as interpret-as='spell-out'>CTE</say-as> protocol tomorrow.  George just laid down the law on Lincoln with a big uppercut. Lincoln misses with a uppercut. George is starting to slow down a big. Lincoln is taking quite a few hits. Lincoln is starting to slow down a big.

            # add did_hit to the topics -> duh
            if gs[ANNOUNCE] == ANNOUNCEGameOver:
                break
