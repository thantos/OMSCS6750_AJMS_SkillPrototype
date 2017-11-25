"""Test cases for Game State Loader."""
from unittest import TestCase
from .game_state_loader import GameStateLoader
from qp import STATS


class GameStateLoadersTests(TestCase):
    """Test all base stations."""

    test_station_1_name = "station1"
    test_station_2_name = "station2"
    test_ship_stat = STATS.ATTACK_POWER
    test_ship_stat_value = 1
    test_opponent_stat = STATS.DODGE
    test_opponent_stat_value = 1
    test_opponent_name = "big ship"
    test_crew_name = "Amy"

    def setUp(self):
        """Setup."""
        self.undertest = GameStateLoader()
        self.stateTest = {
            "ship": {
                "stations": {
                    self.test_station_1_name: {
                        "fire": 0,
                        "damaged": False
                    }, self.test_station_2_name: {
                        "fire": 1,
                        "damaged": True
                    }
                },
                "stats": {
                    self.test_ship_stat: self.test_ship_stat_value
                },
                "crew": {
                    self.test_crew_name: {
                        "station": self.test_station_1_name
                        }
                }
            },
            "stage": {
                "opponent": {
                    "name": self.test_opponent_name,
                    "stats": {
                        self.test_opponent_stat: self.test_opponent_stat_value
                    }
                }
            }
        }

    def test_should_load_full_game_state(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIsNotNone(game_state)

    def test_should_load_ship(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIsNotNone(game_state.ship)

    def test_should_raise_ValueError_when_ship_is_missing(self):
        with self.assertRaises(ValueError):
            self.undertest.loadGameState({})

    def test_should_return_none_stage_when_stage_is_missing(self):
        del self.stateTest['stage']
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIsNone(game_state.stage)

    def test_should_raise_ValueError_when_stations_is_missing(self):
        del self.stateTest['ship']['stations']
        with self.assertRaises(ValueError):
            self.undertest.loadGameState(self.stateTest)

    def test_should_raise_ValueError_when_crew_is_missing(self):
        del self.stateTest['ship']['crew']
        with self.assertRaises(ValueError):
            self.undertest.loadGameState(self.stateTest)

    def test_should_return_empty_when_ship_stats_is_missing(self):
        del self.stateTest['ship']['stats']
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertDictEqual({}, game_state.ship.stats)

    def test_should_load_ship_stations(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        stations = game_state.ship.stations
        self.assertIn(self.test_station_1_name, stations)
        self.assertIn(self.test_station_2_name, stations)

    def test_should_load_ship_station_values(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        stations = game_state.ship.stations
        self.assertEqual(0, stations[self.test_station_1_name].fire)
        self.assertEqual(1, stations[self.test_station_2_name].fire)
        self.assertEqual(False, stations[self.test_station_1_name].damaged)
        self.assertEqual(True, stations[self.test_station_2_name].damaged)

    def test_should_default_when_station_is_none(self):
        self.stateTest['ship']['stations'][self.test_station_2_name] = None
        game_state = self.undertest.loadGameState(self.stateTest)
        stations = game_state.ship.stations
        self.assertEqual(0, stations[self.test_station_2_name].fire)
        self.assertEqual(False, stations[self.test_station_2_name].damaged)

    def test_should_default_fire_to_0_when_missing(self):
        del self.\
            stateTest['ship']['stations'][self.test_station_2_name]['fire']
        game_state = self.undertest.loadGameState(self.stateTest)
        stations = game_state.ship.stations
        self.assertEqual(0, stations[self.test_station_2_name].fire)

    def test_should_default_damage_to_False_when_missing(self):
        del self.\
            stateTest['ship']['stations'][self.test_station_2_name]['damaged']
        game_state = self.undertest.loadGameState(self.stateTest)
        stations = game_state.ship.stations
        self.assertEqual(False, stations[self.test_station_2_name].damaged)

    def test_should_load_ship_stats(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertDictContainsSubset({
            self.test_ship_stat: self.test_ship_stat_value
        }, game_state.ship.stats)

    def test_should_load_ship_crew(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIn(self.test_crew_name, game_state.ship.crew)

    def test_should_load_ship_crew_station(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertEquals(
            self.test_station_1_name,
            game_state.ship.crew[self.test_crew_name].station)

    def test_should_default_ship_crew_station_to_None_when_missing(self):
        del self.stateTest['ship']['crew'][self.test_crew_name]['station']
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIsNone(game_state.ship.crew[self.test_crew_name].station)

    def test_should_load_ship_stage(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIsNotNone(game_state.stage)

    def test_should_load_ship_stage_opponent(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIsNotNone(game_state.stage.opponent)

    def test_should_default_opponent_stats_to_none_when_missing(self):
        del self.stateTest['stage']['opponent']
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIsNone(game_state.stage.opponent)

    def test_should_load_ship_stage_opponent_values(self):
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertEqual(
            self.test_opponent_name, game_state.stage.opponent.name)
        self.assertDictContainsSubset(
            {self.test_opponent_stat: self.test_opponent_stat_value},
            game_state.stage.opponent.stats)

    def test_should_default_opponent_stats_to_empty_when_mising(self):
        del self.stateTest['stage']['opponent']['stats']
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertDictEqual({}, game_state.stage.opponent.stats)

    def test_should_default_opponent_name_None_when_mising(self):
        del self.stateTest['stage']['opponent']['name']
        game_state = self.undertest.loadGameState(self.stateTest)
        self.assertIsNone(game_state.stage.opponent.name)
