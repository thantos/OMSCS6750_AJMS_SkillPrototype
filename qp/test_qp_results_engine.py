from unittest import TestCase
from qp_result_engine import QPResultEngine
from qp import STATS


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
