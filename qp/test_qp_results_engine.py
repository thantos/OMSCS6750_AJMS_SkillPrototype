""""""
from unittest import TestCase
from qp_result_engine import QPResultEngine
from qp import STATS, HullDestroyed, LifeSupportDepleted
from qp.state import StationState, CrewMemberState
from .qp_combat_results import StationFireStateChange, \
    StationStateActor, StationDamageStateChange


class TestQPResultEngine(TestCase):

    def test_calculate_threshold_should_find_upper_threshold(self):
        (up, result) = \
            QPResultEngine._QPResultEngine__calculate_threshold(
                10, 20, 20, {
                    "FULL": 100,
                    "MID": 75})

        self.assertTrue(up)
        self.assertEqual("FULL", result)

    def test_calculate_threshold_should_find_lower_threshold(self):
        (up, result) = \
            QPResultEngine._QPResultEngine__calculate_threshold(
                20, 10, 20, {
                    "FULL": 100,
                    "MID": 75})

        self.assertFalse(up)
        self.assertEqual("MID", result)

    def test_calculate_threshold_should_handle_same(self):
        (up, result) = \
            QPResultEngine._QPResultEngine__calculate_threshold(
                20, 20, 20, {
                    "FULL": 100,
                    "MID": 75})

        self.assertIsNone(up)
        self.assertIsNone(result)

    def test_calculate_threshold_should_handle_with_threshold_down(self):
        (up, result) = \
            QPResultEngine._QPResultEngine__calculate_threshold(
                75, 74, 100, {
                    "FULL": 100,
                    "MID": 75})

        self.assertFalse(up)
        self.assertIsNone(result)

    def test_calculate_threshold_should_handle_with_threshold_down_2(self):
        (up, result) = \
            QPResultEngine._QPResultEngine__calculate_threshold(
                78, 77, 100, {
                    "FULL": 100,
                    "MID": 75})

        self.assertFalse(up)
        self.assertIsNone(result)

    def test_calculate_threshold_should_handle_with_threshold_up(self):
        (up, result) = \
            QPResultEngine._QPResultEngine__calculate_threshold(
                75, 76, 100, {
                    "FULL": 100,
                    "MID": 75})

        self.assertTrue(up)
        self.assertIsNone(result)

    def test_calculate_threshold_should_handle_no_thresholds(self):
        (up, result) = \
            QPResultEngine._QPResultEngine__calculate_threshold(
                75, 76, 100, {})

        self.assertTrue(up)
        self.assertIsNone(result)

    def test_calculate_threshold_should_handle_no_thresholds_down(self):
        (up, result) = \
            QPResultEngine._QPResultEngine__calculate_threshold(
                75, 74, 100, {})

        self.assertFalse(up)
        self.assertIsNone(result)

    def test_record_stat_threshold_should_show_drop_in_HH(self):
        results = QPResultEngine().record_stat_threshold(
            *self.__create_stats(50, 10, 20, 20, 20, 20, 100)
        )

        self.assertEquals(1, len(results))
        self.assertEquals("LOW", results[0].threshold)
        self.assertFalse(results[0].up)

    def test_record_stat_threshold_should_show_drop_in_LS(self):
        results = QPResultEngine().record_stat_threshold(
            *self.__create_stats(50, 50, 50, 10, 20, 20, 100)
        )

        self.assertEquals(1, len(results))
        self.assertEquals("LOW", results[0].threshold)
        self.assertFalse(results[0].up)

    def test_record_stat_threshold_should_show_drop_in_opp_HH(self):
        results = QPResultEngine().record_stat_threshold(
            *self.__create_stats(50, 50, 50, 50, 100, 75, 100)
        )

        self.assertEquals(1, len(results))
        self.assertEquals("HIGH", results[0].threshold)
        self.assertFalse(results[0].up)

    def test_record_stat_threshold_should_show_drop_in_all(self):
        results = QPResultEngine().record_stat_threshold(
            *self.__create_stats(75, 50, 50, 25, 100, 75, 100)
        )

        self.assertEquals(3, len(results))
        self.assertEquals("MID", results[0].threshold)
        self.assertEquals("LOW", results[2].threshold)
        self.assertEquals("HIGH", results[1].threshold)

    def __create_stats(self, S_HH, E_HH, S_LS, E_LS, S_HH_O, E_HH_O, M):
        return (
            {
                STATS.HULL_HEALTH: S_HH,
                STATS.MAX_HULL_HEALTH: M,
                STATS.LIFE_SUPPORT: S_LS,
                STATS.MAX_LS: M
            },
            {
                STATS.HULL_HEALTH: E_HH,
                STATS.MAX_HULL_HEALTH: M,
                STATS.LIFE_SUPPORT: E_LS,
                STATS.MAX_LS: M
            },
            {
                STATS.HULL_HEALTH: S_HH_O,
                STATS.MAX_HULL_HEALTH: M
            },
            {
                STATS.HULL_HEALTH: E_HH_O,
                STATS.MAX_HULL_HEALTH: M
            }
        )


class QPResultEngineEndGameTests(TestCase):
    """"""
    test_game_state = None

    def setUp(self):
        self.undertest = QPResultEngine()
        self.player_stats = {
                STATS.HULL_HEALTH: 10,
                STATS.LIFE_SUPPORT: 10
            }
        self.opponent_stats = {
                STATS.HULL_HEALTH: 10
            }

    def test_should_have_no_end_game(self):
        result = self.undertest.record_end_game(
            self.player_stats, self.opponent_stats)

        self.assertEqual(0, len(result))

    def test_should_have_player_hull_end_game_when_hull_0(self):
        self.player_stats[STATS.HULL_HEALTH] = 0

        result = self.undertest.record_end_game(
            self.player_stats, self.opponent_stats)

        self.assertIsInstance(result[0], HullDestroyed)
        self.assertTrue(result[0].player)

    def test_should_have_player_hull_end_game_when_hull_less_than_0(self):
        self.player_stats[STATS.HULL_HEALTH] = -10

        result = self.undertest.record_end_game(
            self.player_stats, self.opponent_stats)

        self.assertIsInstance(result[0], HullDestroyed)

    def test_should_have_life_support_end_game_when_ls_0(self):
        self.player_stats[STATS.LIFE_SUPPORT] = 0

        result = self.undertest.record_end_game(
            self.player_stats, self.opponent_stats)

        self.assertIsInstance(result[0], LifeSupportDepleted)

    def test_should_have_life_support_end_game_when_ls_less_than_0(self):
        self.player_stats[STATS.LIFE_SUPPORT] = -10

        result = self.undertest.record_end_game(
            self.player_stats, self.opponent_stats)

        self.assertIsInstance(result[0], LifeSupportDepleted)

    def test_should_have_opponent_hull_end_game_when_hull_0(self):
        self.opponent_stats[STATS.HULL_HEALTH] = 0

        result = self.undertest.record_end_game(
            self.player_stats, self.opponent_stats)

        self.assertIsInstance(result[0], HullDestroyed)
        self.assertFalse(result[0].player)

    def test_should_have_opponent_hull_end_game_when_hull_less_than_0(self):
        self.opponent_stats[STATS.HULL_HEALTH] = -10

        result = self.undertest.record_end_game(
            self.player_stats, self.opponent_stats)

        self.assertIsInstance(result[0], HullDestroyed)

    def test_should_have_fire_extinguished(self):
        result = self.undertest.record_station_advance_result({
                "AUTO_TURRET": StationState(fire=10)}, {
                "AUTO_TURRET": StationState(fire=0)}, {
                "AUTO_TURRET": StationState(fire=0)}, {
                    "LESTER": CrewMemberState(station="AUTO_TURRET")
                })

        self.assertIsInstance(result[0], StationFireStateChange)
        self.assertEqual(result[0].extinguished_by, "LESTER")

    def test_should_have_fire_extinguished_and_started(self):
        result = self.undertest.record_station_advance_result({
                "AUTO_TURRET": StationState(fire=10)}, {
                "AUTO_TURRET": StationState(fire=0)}, {
                "AUTO_TURRET": StationState(fire=1)}, {
                    "LESTER": CrewMemberState(station="AUTO_TURRET")
                })

        self.assertIsInstance(result[0], StationFireStateChange)
        self.assertEqual(result[0].extinguished_by, "LESTER")
        self.assertEqual(result[0].start_by, StationStateActor.ATTACK)

    def test_should_have_fire_started(self):
        result = self.undertest.record_station_advance_result({
                "AUTO_TURRET": StationState(fire=0)}, {
                "AUTO_TURRET": StationState(fire=0)}, {
                "AUTO_TURRET": StationState(fire=1)}, {
                    "LESTER": CrewMemberState(station="AUTO_TURRET")
                })

        self.assertIsInstance(result[0], StationFireStateChange)
        self.assertIsNone(result[0].extinguished_by)
        self.assertEqual(result[0].start_by, StationStateActor.ATTACK)

    def test_should_have_damaged_by_attack(self):
        result = self.undertest.record_station_advance_result({
                "AUTO_TURRET": StationState(damaged=False)}, {
                "AUTO_TURRET": StationState(damaged=False)}, {
                "AUTO_TURRET": StationState(damaged=True)}, {
                    "LESTER": CrewMemberState(station="AUTO_TURRET")
                })

        self.assertIsInstance(result[0], StationDamageStateChange)
        self.assertIsNone(result[0].repaired_by)
        self.assertEqual(result[0].damaged_by, StationStateActor.ATTACK)

    def test_should_have_damaged_by_fire(self):
        result = self.undertest.record_station_advance_result({
                "AUTO_TURRET": StationState(fire=1, damaged=False)}, {
                "AUTO_TURRET": StationState(fire=1, damaged=True)}, {
                "AUTO_TURRET": StationState(fire=1, damaged=True)}, {
                    "LESTER": CrewMemberState(station="AUTO_TURRET")
                })

        self.assertIsInstance(result[0], StationDamageStateChange)
        self.assertIsNone(result[0].repaired_by)
        self.assertEqual(result[0].damaged_by, StationStateActor.FIRE)

    def test_should_have_repaired_by(self):
        result = self.undertest.record_station_advance_result({
                "AUTO_TURRET": StationState(damaged=True)}, {
                "AUTO_TURRET": StationState()}, {
                "AUTO_TURRET": StationState()}, {
                    "LESTER": CrewMemberState(station="AUTO_TURRET")
                })

        self.assertIsInstance(result[0], StationDamageStateChange)
        self.assertEqual(result[0].repaired_by, "LESTER")
        self.assertIsNone(result[0].damaged_by)

    def test_should_have_no_state_change(self):
        result = self.undertest.record_station_advance_result({
                "AUTO_TURRET": StationState(damaged=True)}, {
                "AUTO_TURRET": StationState(damaged=True)}, {
                "AUTO_TURRET": StationState(damaged=True)}, {
                    "LESTER": CrewMemberState(station="AUTO_TURRET")
                })

        self.assertEqual(0, len(result))
