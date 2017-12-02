from unittest import TestCase
from boxer import *
from match import *
from boxing_strings import *


def add_to_history(gs, moves, player=True):
    for move in moves:
        if player:
            gs[PLAYERHISTORY].append(move)
        else:
            gs[OPPONENTHISTORY].append(move)


class TestBonus(TestCase):
    def test_bonus_uppercut(self):
        gs = initialize({})
        add_to_history(gs, [(MOVEuppercut, True)], player=True)
        add_to_history(gs, [(MOVEuppercut, True)], player=False)
        self.assertEqual(bonus(gs, True), ADdisadvantage)
        self.assertEqual(bonus(gs, False), ADdisadvantage)

    def test_nobonus_uppercut(self):
        gs = initialize({})
        add_to_history(gs, [(MOVEuppercut, False)], player=True)
        add_to_history(gs, [(MOVEuppercut, True)], player=False)
        self.assertEqual(bonus(gs, True), ADNobonus)
        self.assertEqual(bonus(gs, False), ADdisadvantage)

    def test_bonus_taunt_granted(self):
        gs = initialize({})
        add_to_history(gs, [(MOVEtaunt, True)], player=True)
        add_to_history(gs, [(MOVEjab, False)], player=False)
        self.assertEqual(bonus(gs, True), ADsuper)
        self.assertEqual(bonus(gs, False), ADNobonus)

    def test_adv_on_wrapup(self):
        gs = initialize({})
        add_to_history(gs, [(MOVEwrapup, True)], player=True)
        add_to_history(gs, [(MOVEjab, False)], player=False)
        self.assertEqual(bonus(gs, True), ADadvantage)
        self.assertEqual(bonus(gs, False), ADNobonus)

    def test_bonus_taunt_not_granted(self):
        gs = initialize({})

        # no taunt if the opp lands a punch when you taunt
        add_to_history(gs, [(MOVEtaunt, True)], player=True)
        add_to_history(gs, [(MOVEjab, True)], player=False)
        self.assertEqual(bonus(gs, True), ADNobonus)
        self.assertEqual(bonus(gs, False), ADNobonus)

    def test_heating_up(self):
        # advantage for two hits in a row
        attack_moves = [MOVEjab, MOVEhook, MOVEuppercut, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                gs = initialize({})
                gs[CURRENTTURN] = 2
                add_to_history(gs, [(move, True), (move2, True)], player=True)
                add_to_history(gs, [(move, False), (move2, False)], player=False)

                self.assertEqual(bonus(gs, True), ADadvantage)
                self.assertEqual(bonus(gs, False), ADNobonus)

    def test_not_heating_up(self):
        # no advantage when you miss
        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                gs = initialize({})
                add_to_history(gs, [(move, True), (move2, False)], player=True)
                add_to_history(gs, [(move, False), (move2, False)], player=False)
                self.assertEqual(bonus(gs, True), ADNobonus)
                self.assertEqual(bonus(gs, False), ADNobonus)

    def test_not_heating_up2(self):
        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                gs = initialize({})
                add_to_history(gs, [(move, False), (move2, True)], player=True)
                add_to_history(gs, [(move, False), (move2, False)], player=False)
                self.assertEqual(bonus(gs, True), ADNobonus)
                self.assertEqual(bonus(gs, False), ADNobonus)

    def test_not_heating_up3(self):
        # no advantage when you miss
        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                gs = initialize({})
                add_to_history(gs, [(move, True), (move2, True)], player=True)
                add_to_history(gs, [(move, True), (move2, False)], player=False)
                self.assertEqual(bonus(gs, True), ADNobonus)
                self.assertEqual(bonus(gs, False), ADNobonus)

    def test_not_heating_up4(self):
        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                gs = initialize({})
                add_to_history(gs, [(move, True), (move2, True)], player=True)
                add_to_history(gs, [(move, False), (move2, True)], player=False)
                self.assertEqual(bonus(gs, True), ADNobonus)
                self.assertEqual(bonus(gs, False), ADNobonus)

    def test_heating_up_three(self):

        # advantage for two hits in a row
        attack_moves = [MOVEjab, MOVEhook, MOVEcross, MOVEuppercut]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    gs = initialize({})
                    add_to_history(gs, [(move, False), (move2, True), (move3, True)], player=True)
                    add_to_history(gs, [(move, False), (move2, False), (move3, False)], player=False)

                    self.assertEqual(bonus(gs, True), ADadvantage)
                    self.assertEqual(bonus(gs, False), ADNobonus)

    def test_heating_up_three(self):

        # advantage for two hits in a row
        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    gs = initialize({})
                    add_to_history(gs, [(move, False), (move2, True), (move3, True)], player=True)
                    add_to_history(gs, [(move, False), (move2, True), (move3, False)], player=False)

                    self.assertEqual(bonus(gs, True), ADNobonus)
                    self.assertEqual(bonus(gs, False), ADNobonus)

    def test_heating_up_after_hit(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    for move4 in attack_moves:
                        gs = initialize({})
                        gs[CURRENTTURN] = 4
                        add_to_history(gs, [(move, True), (move2, True), (move3, True), (move4, True)], player=True)
                        add_to_history(gs, [(move, False), (move2, True), (move3, False), (move4, False)],
                                       player=False)

                        self.assertEqual(bonus(gs, True), ADadvantage)
                        self.assertEqual(bonus(gs, False), ADNobonus)

    def test_on_fire(self):

        # on fire when you land three
        attack_moves = [MOVEjab, MOVEhook, MOVEuppercut, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    gs = initialize({})
                    gs[CURRENTTURN] = 3
                    add_to_history(gs, [(move, True), (move2, True), (move3, True)], player=True)
                    add_to_history(gs, [(move, False), (move2, False), (move3, False)], player=False)

                    self.assertEqual(bonus(gs, True), ADOnfire)
                    self.assertEqual(bonus(gs, False), ADNobonus)

    def test_not_on_fire1(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    gs = initialize({})
                    gs[CURRENTTURN] = 3
                    add_to_history(gs, [(move, True), (move2, True), (move3, False)], player=True)
                    add_to_history(gs, [(move, False), (move2, False), (move3, False)], player=False)

                    self.assertEqual(bonus(gs, True), ADNobonus)
                    self.assertEqual(bonus(gs, False), ADNobonus)

    def test_not_on_fire2(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    gs = initialize({})
                    gs[CURRENTTURN] = 3
                    add_to_history(gs, [(move, True), (move2, False), (move3, True)], player=True)
                    add_to_history(gs, [(move, False), (move2, False), (move3, False)], player=False)

                    self.assertEqual(bonus(gs, True), ADNobonus)
                    self.assertEqual(bonus(gs, False), ADNobonus)

    def test_stay_on_fire(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    for move4 in attack_moves:
                        gs = initialize({})
                        gs[CURRENTTURN] = 4
                        add_to_history(gs, [(move, True), (move2, True), (move3, True), (move4, True)], player=True)
                        add_to_history(gs, [(move, False), (move2, False), (move3, False), (move4, False)],
                                       player=False)

                        self.assertEqual(bonus(gs, True), ADOnfire)
                        self.assertEqual(bonus(gs, False), ADNobonus)

    def test_lose_fire(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    for move4 in attack_moves:
                        gs = initialize({})
                        gs[CURRENTTURN] = 4
                        add_to_history(gs, [(move, True), (move2, True), (move3, True), (move4, False)], player=True)
                        add_to_history(gs, [(move, False), (move2, False), (move3, False), (move4, False)],
                                       player=False)

                        self.assertEqual(bonus(gs, True), ADNobonus)
                        self.assertEqual(bonus(gs, False), ADNobonus)

    def test_lose_fire_from_attack1(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    for move4 in attack_moves:
                        gs = initialize({})
                        add_to_history(gs, [(move, True), (move2, True), (move3, True), (move4, True)], player=True)
                        add_to_history(gs, [(move, False), (move2, False), (move3, False), (move4, True)],
                                       player=False)

                        self.assertEqual(bonus(gs, True), ADNobonus)
                        self.assertEqual(bonus(gs, False), ADNobonus)

    def test_lose_fire_from_attack2(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    for move4 in attack_moves:
                        gs = initialize({})
                        add_to_history(gs, [(move, True), (move2, True), (move3, True), (move4, True)], player=True)
                        add_to_history(gs, [(move, False), (move2, False), (move3, True), (move4, False)],
                                       player=False)

                        self.assertEqual(bonus(gs, True), ADNobonus)
                        self.assertEqual(bonus(gs, False), ADNobonus)

    def test_dont_lose_first_until_hit(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        defense_moves = [MOVEbob, MOVEprotect, MOVEfootwork, MOVEhandsup]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    for move4 in defense_moves:
                        for move5 in defense_moves:
                            gs = initialize({})
                            gs[CURRENTTURN] = 5
                            gs[PLAYERBONUS] = ADOnfire
                            add_to_history(gs,
                                           [(move, True), (move2, True), (move3, True), (move4, True), (move5, False)],
                                           player=True)
                            add_to_history(gs,
                                           [(move, False), (move2, False), (move3, True), (move4, True), (move5, True)],
                                           player=False)

                            self.assertEqual(bonus(gs, True), ADOnfire)
                            self.assertEqual(bonus(gs, False), ADNobonus)

    def test_dont_lose_first_until_hit2(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross]
        defense_moves = [MOVEbob, MOVEprotect, MOVEfootwork, MOVEhandsup]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    for move4 in defense_moves:
                        for move5 in attack_moves:
                            gs = initialize({})
                            gs[CURRENTTURN] = 5
                            gs[PLAYERBONUS] = ADOnfire
                            add_to_history(gs, [(move, True), (move2, True), (move3, True), (move4, True),
                                                (move5, False)], player=True)
                            add_to_history(gs, [(move, False), (move2, False), (move3, True), (move4, True),
                                                (move5, False)],
                                           player=False)

                            self.assertEqual(bonus(gs, True), ADOnfire)
                            self.assertEqual(bonus(gs, False), ADNobonus)

    def test_dont_lose_first_until_hit3(self):

        attack_moves = [MOVEjab, MOVEhook, MOVEcross, MOVEuppercut]
        for move in attack_moves:
            for move2 in attack_moves:
                for move3 in attack_moves:
                    for move4 in attack_moves:
                        for move5 in attack_moves:
                            gs = initialize({})
                            gs[CURRENTTURN] = 5
                            gs[PLAYERBONUS] = ADOnfire
                            add_to_history(gs, [(move, True), (move2, True), (move3, True), (move4, True),
                                                (move5, False)], player=True)
                            add_to_history(gs, [(move, False), (move2, False), (move3, True), (move4, False),
                                                (move5, False)],
                                           player=False)

                            self.assertEqual(bonus(gs, True), ADOnfire)
                            self.assertEqual(bonus(gs, False), ADNobonus)

    def test_lose_fire_after_bell(self):
        gs = initialize({})
        gs[CURRENTROUND] = 2
        gs[PLAYERBONUS] = ADOnfire
        add_to_history(gs, [(MOVEjab, True), (MOVEjab, True), (MOVEjab, True)], player=True)
        add_to_history(gs, [(MOVEjab, False), (MOVEjab, False), (MOVEjab, False)], player=False)
        self.assertEqual(bonus(gs, True), ADNobonus)

    def test_nobody_should_be_onfire(self):
        gs = initialize({})
        gs[CURRENTROUND] = 1
        gs[CURRENTTURN] = 4
        gs[PLAYERBONUS] = ADOnfire
        add_to_history(gs, [(MOVEuppercut, False), (MOVEjab, False), (MOVEjab, False), (MOVEfootwork, False)], player=True)
        add_to_history(gs, [(MOVEfeint, True), (MOVEjab, False), (MOVEhandsup, False), (MOVEuppercut, True)], player=False)
        self.assertEqual(bonus(gs, True), ADNobonus)
        self.assertEqual(bonus(gs, False), ADdisadvantage)
