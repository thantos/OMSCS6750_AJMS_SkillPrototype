""""""
from unittest import TestCase
from .qp_strings import QPContent
from state import StationState
from stations import STATIONS
from .qp_constants import END_GAME_STATES


class QPContentTests(TestCase):
    """"""

    test_hull = 10
    test_warp = 8
    test_ls = 8
    test_ehull = 6

    def test_p_adv_game_state_response_should_contain_station_state(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull, {
                "AUTO_TURRET": StationState(fire=1),
                "COCKPIT": StationState(fire=1, damaged=True),
                "LIFE_SUPPORT": StationState(),
                "ENGINES": StationState(damaged=True)}, None)

        self.assertIn(STATIONS.get("AUTO_TURRET").name, response.text)
        self.assertIn(STATIONS.get("COCKPIT").name, response.text)
        self.assertIn(STATIONS.get("ENGINES").name, response.text)
        self.assertNotIn(STATIONS.get("LIFE_SUPPORT").name, response.text)

    def test_p_adv_game_state_response_should_report_hull_health(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull,
            {}, None)

        self.assertIn(str(self.test_hull), response.text)
        self.assertIn("The hull has " + str(self.test_hull), response.text)

    def test_p_adv_game_state_response_should_report_ls(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull,
            {}, None)

        self.assertIn(str(self.test_ls), response.text)
        self.assertIn("The life support is charged to " + str(self.test_ls),
                      response.text)

    def test_p_adv_game_state_response_should_report_warp(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull,
            {}, None)

        self.assertIn(str(self.test_warp), response.text)
        self.assertIn("The warp is charged to " + str(self.test_warp),
                      response.text)

    def test_p_adv_game_state_response_should_report_ehull(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull,
            {}, None)

        self.assertIn(str(self.test_warp), response.text)
        self.assertIn("The warp is charged to " + str(self.test_warp),
                      response.text)

    def test_p_adv_game_state_response_should_report_hull_d_end_game(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull,
            {}, None)

        self.assertIn(str(self.test_warp), response.text)
        self.assertIn("The warp is charged to " + str(self.test_warp),
                      response.text)

    def test_p_adv_game_state_response_should_report_hull_destroyed_eg(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull,
            {}, END_GAME_STATES.PLAYER_HULL_DESTROYED)

        self.assertIn("The hull has been destroyed", response.text)

    def test_p_adv_game_state_response_should_report_life_support_eg(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull,
            {}, END_GAME_STATES.PLAYER_LIFE_SUPPORT_LOSS)

        self.assertIn("Life support reserves is empty. ", response.text)

    def test_p_adv_game_state_response_should_report_enemy_hull_eg(self):
        response = QPContent.report_post_advance_state_response(
            self.test_hull, self.test_ls, self.test_warp, self.test_ehull,
            {}, END_GAME_STATES.OPPONENT_HULL_DESTROYED)

        self.assertIn("The enemy ship bursts apart", response.text)
