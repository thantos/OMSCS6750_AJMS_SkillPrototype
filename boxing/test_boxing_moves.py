from unittest import TestCase

from boxer import *
from match import *
from boxing_strings import *
from modifiers import *


class TestMoves(TestCase):
    def setUp(self):
        self.attack_moves = [MOVEcross, MOVEhook, MOVEjab, MOVEuppercut]
        self.defense_moves = [MOVEbob, MOVEfootwork, MOVEhandsup, MOVEprotect]
        self.moves = [MOVEjab, MOVEcross, MOVEhook, MOVEuppercut, MOVEwrapup, MOVEfeint, MOVEtaunt, MOVEbob,
                      MOVEfootwork, MOVEhandsup, MOVEprotect]

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
        gs = initialize({PLAYERMOVE: MOVEcross})
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

    # bonuses should clear each round
    def test_bonuses_cleared(self):
        gs = initialize({PLAYERMOVE: MOVEjab})
        gs[OPPONENTMOVE] = MOVEjab
        gs[PLAYERBONUS] = ADexhausted
        gs[OPPONENTBONUS] = ADexhausted
        gs = update(gs)
        self.assertEqual(gs[PLAYERBONUS], ADNobonus)
        self.assertEqual(gs[OPPONENTBONUS], ADNobonus)

    # test that bonuses get applied - taunt etc
    def test_taunt(self):
        gs = initialize({PLAYERMOVE: MOVEtaunt})
        gs[OPPONENTMOVE] = MOVEcross
        gs[OPPONENTBONUS] = ADexhausted

        gs = update(gs)
        self.assertEqual(gs[PLAYERBONUS], ADsuper)
        self.assertEqual(gs[OPPONENTBONUS], ADNobonus)

    # if you block and the other player misses you get advantage
    def test_block_advantage(self):

        for m in self.defense_moves:
            gs = initialize({PLAYERMOVE: m})
            gs[OPPONENTMOVE] = MOVEcross
            gs[OPPONENTBONUS] = ADexhausted  # ensure opp misses

            gs = update(gs)
            self.assertEqual(gs[PLAYERBONUS], ADadvantage)
            self.assertEqual(gs[OPPONENTBONUS], ADNobonus)

    # if you throw an uppercut you become disadvantaged
    def test_uppercut_bonus(self):

        gs = initialize({PLAYERMOVE: MOVEuppercut})
        for m in self.moves:
            gs[OPPONENTMOVE] = m
            gs[OPPONENTBONUS] = ADexhausted  # ensure opp misses

            gs = update(gs)
            self.assertEqual(gs[PLAYERBONUS], ADdisadvantage)

    # round transitions etc
    def test_alexa_prompts(self):
        gs = initialize({PLAYERMOVE: MOVEtaunt})
        gs[OPPONENTMOVE] = MOVEtaunt
        gs[TURNS] = [3, 3]
        gs[NUMROUNDS] = 2

        self.assertEqual(gs[ANNOUNCEPrompt], ANNOUNCEIntro)

        for i in range(2):
            gs = update(gs)
            self.assertEqual(gs[ANNOUNCEPrompt], ANNOUNCEMidround)

        gs = update(gs)
        self.assertEqual(gs[ANNOUNCEPrompt], ANNOUNCEBetweenRound)

        for i in range(2):
            gs = update(gs)
            self.assertEqual(gs[ANNOUNCEPrompt], ANNOUNCEMidround)

        gs = update(gs)
        self.assertEqual(gs[ANNOUNCEPrompt], ANNOUNCEGameOver)

    def test_game_over(self):
        gs = initialize({PLAYERMOVE: MOVEuppercut})
        gs[PLAYERBONUS] = ADsuper
        gs[OPPONENTMOVE] = MOVEtaunt
        gs[OPPONENTHP] = 1
        gs = update(gs)
        self.assertEqual(gs[ANNOUNCEPrompt], ANNOUNCEGameOver)

