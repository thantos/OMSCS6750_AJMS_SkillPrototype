from unittest import TestCase

from match import *
from boxing_strings import *
from modifiers import *


class TestMoves(TestCase):
    def setUp(self):
        self.attack_moves = [MOVEcross, MOVEhook, MOVEjab, MOVEuppercut]
        self.defense_moves = [MOVEbob, MOVEfootwork, MOVEhandsup, MOVEprotect]
        self.moves = [MOVEjab, MOVEcross, MOVEhook, MOVEuppercut, MOVEwrapup, MOVEfeint, MOVEtaunt, MOVEbob,
                      MOVEfootwork, MOVEhandsup, MOVEprotect]

    # round transitions etc
    def test_alexa_prompts(self):
        gs = initialize({PLAYERMOVE: MOVEtaunt})
        gs[OPPONENTMOVE] = MOVEtaunt
        gs[TURNS] = [3, 3]
        gs[NUMROUNDS] = 2

        self.assertEqual(gs[ANNOUNCE], ANNOUNCEIntro)

        for i in range(2):
            gs = update(gs)
            self.assertEqual(gs[ANNOUNCE], ANNOUNCEMidround)

        gs = update(gs)
        self.assertEqual(gs[ANNOUNCE], ANNOUNCEBetweenRound)

        for i in range(2):
            gs = update(gs)
            self.assertEqual(gs[ANNOUNCE], ANNOUNCEMidround)

        gs = update(gs)
        self.assertEqual(gs[ANNOUNCE], ANNOUNCEGameOver)

    def test_game_over(self):
        gs = initialize({PLAYERMOVE: MOVEuppercut})
        gs[PLAYERBONUS] = ADsuper
        gs[OPPONENTMOVE] = MOVEtaunt
        gs[OPPONENTHP] = 1
        gs = update(gs)
        self.assertEqual(gs[ANNOUNCE], ANNOUNCEGameOver)

    def test_intro_topics(self):
        gs = initialize({PLAYERMOVE: MOVEuppercut})
        p_tpcs, o_tpcs = gs[TOPICS]
        self.assertEqual(len(p_tpcs), 0)
        self.assertEqual(len(o_tpcs), 0)

    def test_health_topics(self):
        gs = initialize({PLAYERMOVE: MOVEuppercut})
        gs[PLAYERBONUS] = ADsuper
        gs[OPPONENTMOVE] = MOVEjab
        gs[OPPONENTBONUS] = ADexhausted  # ensure opp misses

        # big hit and a miss
        gs2 = update(gs)
        p_tpcs2, o_tpcs2 = gs2[TOPICS]
        self.assertEqual(o_tpcs2, [TOPICMiss])
        self.assertEqual(p_tpcs2, [TOPICBighit])

        # regular hit and a miss
        gs2[PLAYERMOVE] = MOVEjab
        gs2[PLAYERBONUS] = ADsuper
        gs2[OPPONENTBONUS] = ADexhausted  # ensure opp misses
        gs3 = update(gs2)

        p_tpcs3, o_tpcs3 = gs3[TOPICS]
        self.assertEqual(o_tpcs3, [TOPICMiss])
        self.assertEqual(p_tpcs3, [TOPICHit])

        # regular hit and a miss -
        # opp had three misses = hard to hit other guy is hard to hit
        # opp health falls into ok
        gs3[PLAYERBONUS] = ADsuper
        gs3[OPPONENTBONUS] = ADexhausted  # ensure opp misses
        gs4 = update(gs3)

        p_tpcs4, o_tpcs4 = gs4[TOPICS]
        self.assertEqual(sorted(o_tpcs4), sorted([TOPICMiss, TOPICHealthok]))
        self.assertEqual(p_tpcs4, [TOPICHardtohit])

        # regular hit and a miss -
        # opp had three misses = hard to hit other guy is hard to hit
        # opp health falls into ok
        gs4[PLAYERBONUS] = ADsuper
        gs4[OPPONENTBONUS] = ADexhausted  # ensure opp misses
        gs5 = update(gs4)

        p_tpcs5, o_tpcs5 = gs5[TOPICS]
        self.assertEqual(sorted(o_tpcs5), sorted([TOPICMiss, TOPICStaminaok]))
        self.assertEqual(p_tpcs5, [TOPICHardtohit])

        # regular hit and a miss -
        # opp had three misses = hard to hit other guy is hard to hit
        # opp health falls into ok
        gs5[PLAYERMOVE] = MOVEuppercut
        gs5[PLAYERBONUS] = ADsuper
        gs5[OPPONENTBONUS] = ADexhausted  # ensure opp misses
        gs6 = update(gs5)

        p_tpcs6, o_tpcs6 = gs6[TOPICS]
        self.assertEqual(sorted(o_tpcs6), sorted([TOPICMiss]))
        self.assertEqual(sorted(p_tpcs6), sorted([TOPICBighit, TOPICStaminaok]))

        # regular hit and a miss -
        # opp had three misses = hard to hit other guy is hard to hit
        # opp health falls into ok
        gs6[PLAYERBONUS] = ADsuper
        gs6[OPPONENTBONUS] = ADexhausted  # ensure opp misses
        gs7 = update(gs6)

        p_tpcs7, o_tpcs7 = gs7[TOPICS]
        self.assertEqual(sorted(o_tpcs7), sorted([TOPICHealthlow, TOPICMiss]))
        self.assertEqual(sorted(p_tpcs7), sorted([TOPICBighit]))
