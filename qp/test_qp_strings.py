""""""
from unittest import TestCase
from .qp_strings import QPContent
from state import StationState
from stations import STATIONS
from .qp_combat_results import *


class QPContentTests(TestCase):

    """ QP Results """

    def test_handle_qp_results_respone_should_output_fire_station_change(self):
        result = QPContent.handle_qp_results_respone(
            [StationFireStateChange(
                "AUTO_TURRET", start_by=StationStateActor.ATTACK)])

        self.assertIn("Auto Turret", result[0].text, result[0].text)

    def test_handle_qp_results_respone_should_output_fire_station_change(self):
        result = QPContent.handle_qp_results_respone(
            [StationFireStateChange(
                "AUTO_TURRET", start_by=None, extinguished_by="LESTER")])

        self.assertIn("Auto Turret", result[0].text, result[0].text)
        self.assertIn("Lester", result[0].text, result[0].text)
