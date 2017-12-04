"""Test for the Quick Particle Game Engine."""
from unittest import TestCase
from qp import QPEngine, STATS
from state import StationState, QPGameState, Ship, CrewMemberState, \
                    StageState, EnemyState
from .qp_exceptions import StationInvalidException, CrewMemberInvalidException
from stations import STATIONS
import mock


class QPEngineInstructCrewTests(TestCase):
    """Test instruct crew operation of QPEngine."""

    test_station = "testStation"
    test_crew_name = "testCrewName"
    test_crew_name2 = "testCrewName2"
    test_station2 = "testStation2"
    test_game_state = QPGameState(
        Ship(
            {
                test_station: StationState(),
                test_station2: StationState()},
            {
                test_crew_name: CrewMemberState(),
                test_crew_name2: CrewMemberState(test_station2)},
            {}
        ), None)

    def setUp(self):
        self.undertest = QPEngine()

    def test_should_move_unassigned_crew_on_instruct(self):
        state = self.undertest.instruct_crew(
            self.test_game_state, self.test_crew_name, self.test_station)

        self.assertEqual(
            self.test_station, state.ship.crew[self.test_crew_name].station)

    def test_should_move_assigned_crew_on_instruct(self):
        state = self.undertest.instruct_crew(
            self.test_game_state, self.test_crew_name2, self.test_station)

        self.assertEqual(
            self.test_station, state.ship.crew[self.test_crew_name2].station)

    def test_should_raise_ValueError_when_game_state_is_not_QPGameState(self):
        with self.assertRaises(ValueError):
            self.undertest.instruct_crew(
                {}, self.test_crew_name2, self.test_station)

    def test_should_raise_CrewMemberInvalidException_when_member_missing(self):
        with self.assertRaises(CrewMemberInvalidException):
            self.undertest.instruct_crew(
                self.test_game_state, "blah", self.test_station)

    def test_should_raise_StationInvalidException_when_member_missing(self):
        with self.assertRaises(StationInvalidException):
            self.undertest.instruct_crew(
                self.test_game_state, self.test_crew_name, "blah")

    def test_should_move_unassigned_crew_on_instruct(self):
        state = self.undertest.instruct_crew(
            self.test_game_state, self.test_crew_name, self.test_station)

        self.assertEqual(
            self.test_station, state.ship.crew[self.test_crew_name].station)


class QPEngineStationStateUpdateTests(TestCase):
    """"""
    test_station = "testStation"
    test_station2 = "testStation2"
    test_station3 = "testStation3"
    test_station4 = "testStation4"
    test_stations = {
        test_station: StationState(),  # No fire, not damaged
        test_station2: StationState(fire=1),  # fire, not damaged
        test_station3: StationState(fire=1, damaged=True),  # fire, damaged
        test_station4: StationState(damaged=True)  # No fire, damaged
    }

    def setUp(self):
        self.undertest = QPEngine()

    def test_one_manned_station_should_not_impact_another(self):
        results = self.undertest._QPEngine__advance_stations_state(
            self.test_stations, [self.test_station2])

        self.assertEquals(results[self.test_station3].fire, 2)

    def test_should_remove_fire_from_manned_station(self):
        results = self.undertest._QPEngine__advance_stations_state(
            self.test_stations, [self.test_station2])

        self.assertEquals(results[self.test_station2].fire, 0)
        self.assertFalse(results[self.test_station2].damaged)

    def test_should_remove_fire_only_from_manned_station(self):
        results = self.undertest._QPEngine__advance_stations_state(
            self.test_stations, [self.test_station3])

        self.assertEquals(results[self.test_station3].fire, 0)
        self.assertTrue(results[self.test_station3].damaged)

    def test_should_repair_damaged_station_when_manned_station(self):
        results = self.undertest._QPEngine__advance_stations_state(
            self.test_stations, [self.test_station4])

        self.assertEquals(results[self.test_station4].fire, 0)
        self.assertFalse(results[self.test_station4].damaged)

    def test_should_not_change_clean_station_when_manned(self):
        results = self.undertest._QPEngine__advance_stations_state(
            self.test_stations, [self.test_station])

        self.assertEquals(results[self.test_station].fire, 0)
        self.assertFalse(results[self.test_station].damaged)

    def test_should_advance_fire_when_on_fire(self):
        results = self.undertest._QPEngine__advance_stations_state(
            self.test_stations, [])

        self.assertEquals(results[self.test_station2].fire, 2)
        self.assertFalse(results[self.test_station2].damaged)

    def test_should_damage_station_when_fire_exceeds_supression(self):
        results = self.undertest._QPEngine__advance_stations_state(
            self.test_stations, [])
        results = self.undertest._QPEngine__advance_stations_state(
            results, [])

        self.assertEquals(results[self.test_station2].fire, 3)
        self.assertTrue(results[self.test_station2].damaged)


class QPEngineAdvanceGeneralTests(TestCase):
    """"""
    test_station = "testStation"
    test_station2 = "testStation2"
    test_station3 = "testStation3"
    test_station4 = "testStation4"
    test_crew1 = "testCrew1"
    test_crew2 = "testCrew2"
    test_crew3 = "testCrew3"
    test_crew = {
        test_crew1: CrewMemberState(test_station),
        test_crew2: CrewMemberState(),
        test_crew3: CrewMemberState(test_station4)
    }
    test_stations = {
        "AUTO_TURRET": StationState(),  # No fire, not damaged
        "COCKPIT": StationState(fire=1),  # fire, not damaged
        "SHIELDS": StationState(damaged=True)  # No fire, damaged
    }

    def setUp(self):
        self.undertest = QPEngine()

    def test_should_collect_manned_stations(self):
        result = self.undertest._QPEngine__get_manned_stations(self.test_crew)
        self.assertEqual(
            set([self.test_station, self.test_station4]), result)

    def test_should_collect_stats_from_stations_not_damaged(self):
        result = self.undertest._QPEngine__collect_stats_from_stations(
            self.test_stations, [])

        self.assertDictContainsSubset(
            STATIONS.get("AUTO_TURRET").handle(False), result)

    def test_should_boost_stat_collected_when_manned(self):
        result = self.undertest._QPEngine__collect_stats_from_stations(
            self.test_stations, ["AUTO_TURRET"])

        self.assertDictContainsSubset(
            STATIONS.get("AUTO_TURRET").handle(True), result)

    def test_should_provide_stats_from_station_on_fire(self):
        result = self.undertest._QPEngine__collect_stats_from_stations(
            self.test_stations, [])

        self.assertDictContainsSubset(
            STATIONS.get("COCKPIT").handle(False), result)

    def test_should_not_boost_stats_from_station_on_fire(self):
        result = self.undertest._QPEngine__collect_stats_from_stations(
            self.test_stations, ["COCKPIT"])

        self.assertDictContainsSubset(
            STATIONS.get("COCKPIT").handle(False), result)

    def test_should_not_provide_stats_when_damaged(self):
        result = self.undertest._QPEngine__collect_stats_from_stations(
            self.test_stations, [])

        self.assertNotIn(STATS.SHIELD, result)

    def test_udpate_stats_should_carry_over_all_stats(self):
        test_stats = {STATS.ATTACK_POWER: 10}
        result = self.undertest._QPEngine__update_stats(
            {}, test_stats)

        self.assertDictEqual(result, test_stats)

    def test_udpate_stats_should_add_to_existing(self):
        test_stats = {STATS.ATTACK_POWER: 10}
        result = self.undertest._QPEngine__update_stats(
            {STATS.ATTACK_POWER: 5}, test_stats)

        self.assertDictEqual(result, {STATS.ATTACK_POWER: 15})

    def test_udpate_stats_should_not_update_ls_beyond_max_ls(self):
        test_stats = {STATS.LIFE_SUPPORT: 10}
        result = self.undertest._QPEngine__update_stats(
            {STATS.MAX_LS: 5}, test_stats)

        self.assertDictContainsSubset({STATS.LIFE_SUPPORT: 5}, result)

    def test_udpate_stats_should_not_update_ls_beyond_max_ls_with_add(self):
        test_stats = {STATS.LIFE_SUPPORT: 10}
        result = self.undertest._QPEngine__update_stats(
            {STATS.MAX_LS: 15, STATS.LIFE_SUPPORT: 10}, test_stats)

        self.assertDictContainsSubset({STATS.LIFE_SUPPORT: 15}, result)

    def test_udpate_stats_should_not_update_ls_beyond_max_hull_health(self):
        test_stats = {STATS.HULL_HEALTH: 10}
        result = self.undertest._QPEngine__update_stats(
            {STATS.MAX_HULL_HEALTH: 5}, test_stats)

        self.assertDictContainsSubset({STATS.HULL_HEALTH: 5}, result)

    def test_udpate_stats_should_not_update_ls_beyond_max_hh_with_add(self):
        test_stats = {STATS.HULL_HEALTH: 10}
        result = self.undertest._QPEngine__update_stats(
            {STATS.MAX_HULL_HEALTH: 15, STATS.HULL_HEALTH: 10}, test_stats)

        self.assertDictContainsSubset({STATS.HULL_HEALTH: 15}, result)

    def test_collect_persistent_stats_should_collect_defined_stats(self):
        test_stats = {
                        value: 10
                        for (key, value) in STATS.__dict__.iteritems()
                        if not key.startswith('__')}

        results = \
            self.undertest._QPEngine__collect_persistent_stats(test_stats)

        self.assertDictEqual({
            STATS.HULL_HEALTH: 10,
            STATS.LIFE_SUPPORT: 10,
            STATS.WARP: 10
        }, results)


class QPEngineCombatTests(TestCase):
    """"""

    def setUp(self):
        self.undertest = QPEngine()

    def test_attack_should_miss_with_0_power(self):
        att, dff = self.__build_stats(acc=10, att=0)
        result = \
            self.undertest._QPEngine__attack(att, dff)
        self.assertEquals(result, 0)

    def test_attack_should_miss_with_0_accuracy(self):
        att, dff = self.__build_stats(acc=0, att=10)
        result = \
            self.undertest._QPEngine__attack(att, dff)
        self.assertEquals(result, 0)

    def test_attack_should_hit(self):
        with mock.patch('random.randint', lambda s, e: 1):
            att, dff = self.__build_stats(acc=4, att=10)
            result = \
                self.undertest._QPEngine__attack(att, dff)
            self.assertEquals(result, 10)

    def test_attack_should_hit_at_exact_hit_chance(self):
        with mock.patch('random.randint', lambda s,e: 10):
            att, dff = self.__build_stats(acc=.1, att=10)
            result = \
                self.undertest._QPEngine__attack(att, dff)
            self.assertEquals(result, 10)

    def test_attack_should_not_hit_at_accuracy_reduce_by_dodge(self):
        with mock.patch('random.randint', lambda s, e: 10):
            att, dff = self.__build_stats(acc=1, att=10, ddg=10)
            result = \
                self.undertest._QPEngine__attack(att, dff)
            self.assertEquals(result, 0)

    def test_attack_should_be_dampended_by_shields(self):
        with mock.patch('random.randint', lambda s, e: 10):
            att, dff = self.__build_stats(acc=1, att=10, sld=9)
            result = \
                self.undertest._QPEngine__attack(att, dff)
            self.assertEquals(result, 1)

    def test_attack_should_not_be_dampended_by_shields_below_0(self):
        with mock.patch('random.randint', lambda s,e: 0):
            att, dff = self.__build_stats(acc=1, att=10, sld=11)
            result = \
                self.undertest._QPEngine__attack(att, dff)
            self.assertEquals(result, 0)

    def test_attack_should_treat_missing_acc_as_0(self):
        with mock.patch('random.randint', lambda s, e: 0):
            att, dff = self.__build_stats()
            result = \
                self.undertest._QPEngine__attack({
                    STATS.ATTACK_POWER: 10}, dff)
            self.assertEquals(result, 0)

    def test_attack_should_treat_missing_att_as_0(self):
        with mock.patch('random.randint', lambda s, e: 1):
            att, dff = self.__build_stats()
            result = \
                self.undertest._QPEngine__attack({
                    STATS.ACCURACY: 10}, dff)
            self.assertEquals(result, 0)

    def test_attack_should_treat_missing_dodge_as_0(self):
        with mock.patch('random.randint', lambda s, e: 1):
            att, dff = self.__build_stats(acc=1, att=10)
            result = \
                self.undertest._QPEngine__attack(att, {
                    STATS.SHIELD: 0})
            self.assertEquals(result, 10)

    def test_attack_should_treat_missing_shield_as_0(self):
        with mock.patch('random.randint', lambda s, e: 1):
            att, dff = self.__build_stats(acc=1, att=10)
            result = \
                self.undertest._QPEngine__attack(att, {
                    STATS.DODGE: 0})
            self.assertEquals(result, 10)

    def test_combat_should_involve_both_ships(self):
        with mock.patch('random.randint', lambda s, e: 1):
            result = \
                self.undertest._QPEngine__combat({
                    STATS.ATTACK_POWER: 10,
                    STATS.ACCURACY: .1,  # Anything greater than 0
                    STATS.SHIELD: 5
                }, {
                    STATS.ATTACK_POWER: 6,
                    STATS.ACCURACY: .1,  # Anything greater than 0
                    STATS.SHIELD: 1})
            self.assertEquals(result, (1, 9))  # 1 = (6 - 5), 9 = (10 - 1)

    def __build_stats(self, att=0, acc=0, ddg=0, sld=0):
        attacker_stats = {
            STATS.ATTACK_POWER: att,
            STATS.ACCURACY: acc
        }
        defender_stats = {
            STATS.DODGE: ddg,
            STATS.SHIELD: sld
        }
        return (attacker_stats, defender_stats)
