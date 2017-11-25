from unittest import TestCase

from boxer import *
from match import *
from boxing_strings import *
from modifiers import *


class TestMoves(TestCase):
    def setUp(self):
        self.attack_moves = [MOVEcross, MOVEhook, MOVEjab, MOVEuppercut]
        self.defense_moves = [MOVEbob, MOVEfootwork, MOVEhandsup, MOVEprotect]
        self.moves = [MOVEjab, MOVEcross, MOVEhook, MOVEuppercut, MOVEwrapup, MOVEfeint, MOVEtaunt, MOVEbob, MOVEfootwork, MOVEhandsup, MOVEprotect]

    # all defense gives a negative modifier - not strict requirement
    def test_defense(self):
        for attack in self.attack_moves:
            for defense in self.defense_moves:
                mod = modifier(attack, defense)
                self.assertTrue(mod < 0)

    # ensure all moves have the same 'cost' independent of hitting
    def test_move_cost(self):
        for m in self.moves:
            hit_res_p, hit_res_o = hit_result(m)
            miss_res_p, miss_res_o = miss_result(m)
            self.assertTrue(hit_res_p == miss_res_p)

    # super always hits
    def test_super(self):
        gs = initialize({PLAYERMOVE:MOVEcross})
        gs[OPPONENTMOVE] = MOVEcross
        gs[PLAYERBONUS] = ADsuper
        for i in range(100):
            does_hit, player_delta, opp_delta = hit(gs)
            self.assertTrue(does_hit)

    # exhausted always misses
    def test_exhausted(self):
        gs = initialize({PLAYERMOVE: MOVEcross})
        gs[OPPONENTMOVE] = MOVEcross
        gs[PLAYERBONUS] = ADexhausted
        for i in range(100):
            does_hit, player_delta, opp_delta = hit(gs)
            self.assertFalse(does_hit)







