from unittest import TestCase
from .qp_skill_adaptor import QPSkillAdaptor
from qp import CREW_MEMBERS, QPRunner, \
    CrewMemberInvalidException, StationInvalidException
from qp.stations import STATIONS
import mock


def create_slot(name, id=None):
    slot = {
          "name": name,
        }
    if id is not None:
        slot["resolutions"] = {
            "resolutionsPerAuthority": [
              {
                "values": [
                  {
                    "value": {
                      "id": id
                    }
                  }
                ]
              }
            ]
          }
    return slot


class QPAdaptorTests(TestCase):

    test_crew = CREW_MEMBERS["LESTER"]
    test_station = STATIONS["COCKPIT"]
    test_station_slot = create_slot("stationSlot", test_station.id)
    test_crew_slot = create_slot("crewSlot", "LESTER")
    test_intent = {
        "name": "instructCrewIntent",
        "slots": {
          "crewSlot": test_crew_slot,
          "stationSlot": test_station_slot
        }
      }

    def setUp(self):
        self.undertest = QPSkillAdaptor()

    def test_should_create_new_game_with_crew_members(self):

        (resp, state) = self.undertest._QPSkillAdaptor__handle_new_game()

        self.assertIsNotNone(state)
        for crew in state.ship.crew.keys():
            self.assertIn(
                CREW_MEMBERS[crew]["name"],
                resp["outputSpeech"]["text"])

    def test_should_create_new_game_with_stations(self):
        (resp, state) = self.undertest._QPSkillAdaptor__handle_new_game()

        self.assertIsNotNone(state)
        for station in state.ship.stations.keys():
            self.assertIn(
                STATIONS[station].name,
                resp["outputSpeech"]["text"])

    def test_should_not_end_game_on_new_game(self):
        (resp, state) = self.undertest._QPSkillAdaptor__handle_new_game()

        self.assertFalse(resp["shouldEndSession"])

    def test_should_extract_id_from_slots(self):
        id = self.undertest._QPSkillAdaptor__extract_id_from_slot(
            create_slot("test", "LESTER"))
        self.assertEqual("LESTER", id)

    def test_extract_id_from_slots_should_return_none_on_failure(self):
        id = self.undertest._QPSkillAdaptor__extract_id_from_slot(
            create_slot("test"))
        self.assertIsNone(id)

    def test_handle_instruct_crew_should_extract_valid_crew(self):
        with mock.patch(
         'qp.QPRunner.instruct_crew',
         lambda s, g, c, st: (1, CREW_MEMBERS[c], STATIONS[st])):
            (resp, state) = \
                self.undertest._QPSkillAdaptor__handle_instruct_crew(
                self.test_intent["slots"], None)

            self.assertIn(
                self.test_crew["name"],
                resp["outputSpeech"]["text"])

            self.assertIn(
                self.test_station.name,
                resp["outputSpeech"]["text"])

    def test_handle_instruct_crew_should_return_error_with_missing_crew(self):
        error = "cm is invalid"

        def __raise(): raise CrewMemberInvalidException(error)
        with mock.patch(
         'qp.QPRunner.instruct_crew',
         lambda s, g, c, st: __raise()):
            (resp, state) = \
                self.undertest._QPSkillAdaptor__handle_instruct_crew(
                self.test_intent["slots"], None)
            self.assertIn(
                error,
                resp["outputSpeech"]["text"])

    def test_handle_instruct_crew_should_return_error_with_missing_st(self):
        error = "station is invalid"

        def __raise(): raise StationInvalidException(error)
        with mock.patch(
         'qp.QPRunner.instruct_crew',
         lambda s, g, c, st: __raise()):
            (resp, state) = \
                self.undertest._QPSkillAdaptor__handle_instruct_crew(
                self.test_intent["slots"], None)
            self.assertIn(
                error,
                resp["outputSpeech"]["text"])
