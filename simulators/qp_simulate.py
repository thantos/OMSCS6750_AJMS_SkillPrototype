""""""
from qp import QPRunner, STATS, BASE_STATS, EndGameState, HullDestroyed, \
    LifeSupportDepleted
import numpy
import random


class QPSimulator(object):

    def __init__(self):
        self.runner = QPRunner()

    def __simulate_start(self, crew_station_strategy):
        game_state = self.runner.new_game(
            2, ["AUTO_TURRET", "COCKPIT", "LIFE_SUPPORT"])

        start_stage = self.runner.start_stage("Destroyer", {
            STATS.HULL_HEALTH: 50,
            STATS.ATTACK_POWER: 5,
            STATS.DODGE: 2,
            STATS.SHIELD: 0,
            STATS.ACCURACY: 4,
            STATS.MAX_HULL_HEALTH: 50
        })

        game_state.ship.stats = \
            self.runner.prime_ship_for_combat(BASE_STATS)

        game_state.stage = start_stage

        is_end_game = False
        round = 0
        while not is_end_game:
            crew_stations = crew_station_strategy(game_state)
            reassign_crew = [c for (c, s) in game_state.ship.crew.iteritems()
                             if s.station not in crew_stations]
            current_stations = \
                [s.station for (c, s) in game_state.ship.crew.iteritems()
                 if s.station is not None]
            reassign_stations = [s for s in crew_stations
                                 if s not in current_stations]
            for i in range(max(len(reassign_crew), len(reassign_stations))):
                (game_state, s, c) = self.runner.instruct_crew(
                    game_state, reassign_crew[i], reassign_stations[i])
            round += 1
            (game_state, qp_results) = \
                self.runner.advance_combat(game_state)
            is_end_game = self.__is_end_game(qp_results)

        return (round, game_state, qp_results)

    def __is_end_game(self, qp_results):
        return len(filter(lambda r: issubclass(
            type(r), EndGameState), qp_results)) > 0

    def simulate_start_at_c_only(self):
        return self.__simulate_start(
            lambda gs: ["COCKPIT", "AUTO_TURRET"])

    def simulate_start_at_ls_only(self):
        return self.__simulate_start(
            lambda gs: ["LIFE_SUPPORT", "AUTO_TURRET"])

    def simulate_start_c_ls_only(self):
        return self.__simulate_start(
            lambda gs: ["LIFE_SUPPORT", "COCKPIT"])

    def simulate_start_random(self):
        return self.__simulate_start(
            lambda gs: random.sample(
                ["LIFE_SUPPORT", "COCKPIT", "AUTO_TURRET"], 2))

    def simulate_start_smartish(self):
        return self.__simulate_start(
            lambda gs: ["AUTO_TURRET"] +
            [("LIFE_SUPPORT"
             if gs.ship.stats[STATS.LIFE_SUPPORT] < 20
             or gs.ship.stations["LIFE_SUPPORT"].fire > 0
             or gs.ship.stations["LIFE_SUPPORT"].damaged
             else "COCKPIT")])

    def simulate_1(self, sim):
        (r, state, qp_results) = sim(self)
        print self.runner.to_json_friendly(state)
        print self.runner.to_json_friendly(qp_results)
        print r

    def simulate_many(self, sim, many):
        runs = [sim(self) for i in range(many)]

        print "--- rounds ---"
        rounds = [r[0] for r in runs]
        self.__stats(rounds)

        self.__end_game_stats(
            "Player Hull Destroyed",
            lambda r: isinstance(r, HullDestroyed) and r.player, runs)
        self.__end_game_stats(
            "Opponent Hull Destroyed",
            lambda r: isinstance(r, HullDestroyed) and not r.player, runs)
        self.__end_game_stats(
            "Player Life Support Depleted",
            lambda r: isinstance(r, LifeSupportDepleted), runs)

    def __stats(self, data):
        if len(data) > 0:
            print "mean:", numpy.mean(data), "median:", numpy.median(data), \
             "max:", numpy.max(data), "min:", numpy.min(data), \
             "count:", len(data)
        else:
            print "No Data Found"

    def __end_game_stats(self, end_game_name, end_game_predicate, runs):
        print "---", end_game_name, "---"
        ph_runs = [r for r in runs
                   if len(filter(end_game_predicate, r[2])) > 0]
        if len(ph_runs) > 0:
            print "---- rounds ----"
            self.__stats([r[0] for r in ph_runs])
            print "---- LS ----"
            self.__stats([r[1].ship.stats[STATS.LIFE_SUPPORT]
                         for r in ph_runs])
            print "---- HH ----"
            self.__stats([r[1].ship.stats[STATS.HULL_HEALTH] for r in ph_runs])
            print "---- eHH ----"
            self.__stats([r[1].stage.opponent.stats[STATS.HULL_HEALTH]
                          for r in ph_runs])
        else:
            print "No Data Found"
