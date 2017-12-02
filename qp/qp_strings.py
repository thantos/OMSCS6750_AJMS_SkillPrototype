"""QP Common Strings Module."""
from skill_helpers import PlainResponse, SSMLResponse, SimpleCard
from stations import STATIONS
from .qp_constants import END_GAME_STATES


class QPContent(object):
    """Common Strings and Text output functions."""

    QUICK_PARTICLE_STRING = "Quick Particle"
    DEFAULT_OUTPUT = "Welcome to quick particle. Content coming soon."
    DEFAULT_RESPONSE = \
        PlainResponse(DEFAULT_OUTPUT)
    DEFAULT_CARD = SimpleCard(QUICK_PARTICLE_STRING, DEFAULT_OUTPUT)

    """
    New Game
    """

    NEW_GAME_INTRO = \
        "Welcome to Quick Particle, no Ship found, generating one."
    NEW_GAME_CARD_TITLE = "Quick Particle Ship Acquisition"
    MOVE_SUGGESTION_TEXT = \
        "You can assign your crew to stations by saying move " \
        + "crew name to station name. Say GO once you are ready " \
        + "to engage the enemy ship."

    @staticmethod
    def list_crew(crew_names):
        return "Your crew is " + (", ".join(crew_names)) + "."

    @staticmethod
    def list_stations(station_names):
        return "The stations you have installed are " + \
            ", ".join(station_names) + "."

    @staticmethod
    def describe_stage(opponent_name):
        return "Captain, there is an enemy ship called " + \
            opponent_name + ". It has begun firing on us." + \
            " We need to get our crew into position."

    # TODO separate new game, stage, and instructions
    @staticmethod
    def new_game_response(crew_members, stations, opponent_name):
        return PlainResponse(
            " ".join([
             QPContent.NEW_GAME_INTRO,
             QPContent.list_crew(crew_members),
             QPContent.list_stations(stations),
             QPContent.describe_stage(opponent_name),
             QPContent.MOVE_SUGGESTION_TEXT]))

    """
    Instruct Crew
    """

    INSTRUCT_CREW_CARD = SimpleCard("Instruct crew member", "")
    INSTRUCT_CREW_REPROMPT = \
        PlainResponse("anymore to move? otherwise say GO when ready.")
    INVALID_INSTRUCTION_CARD = SimpleCard("Invalid Instruction", "")

    @staticmethod
    def instruct_crew_response(crew_name, station_name):
        return PlainResponse(crew_name + " has been moved to " + station_name)

    """
    Crew State
    """
    CREW_STATE_CARD = SimpleCard("Crew State", "")

    @staticmethod
    def cs_station_unmanned_response(station_name):
        return PlainResponse(station_name + " is unmanned.")

    @staticmethod
    def cs_station_not_avaliable_response(station_name):
        return PlainResponse(
            "your ship does not have the " + station_name + " station yet")

    @staticmethod
    def cs_station_is_invalid_response(station_name):
        return PlainResponse(station_name + " is not a valid station")

    @staticmethod
    def cs_crew_not_assigned(crew_name):
        return crew_name + " has not been assigned."

    @staticmethod
    def cs_crew_crew_manning_station(crew_name, station_name):
        return crew_name + " is manning the " + station_name + ". "

    @staticmethod
    def cs_crew_stations_reponse(crew_station_names_tuples):
        return PlainResponse(" ".join(
            [QPContent.cs_crew_crew_manning_station(c, s) if s is not None else
             QPContent.cs_crew_not_assigned(c)
             for (c, s) in crew_station_names_tuples]))

    @staticmethod
    def cs_crew_member_invalid_response(crew_name):
        return PlainResponse(crew_name + " is not in the crew")

    """
    Advance
    """

    @staticmethod
    def report_post_advance_state_response(
     hull, ls, warp, ehull, stations, end_game):
        """Ship state, station state, and end_game states."""
        return PlainResponse(
            " ".join([s for s in [
             "The hull has " + str(hull) + " points remaining. ",
             "The life support is charged to " + str(ls) + ". ",
             "The warp is charged to " + str(warp) + ". ",
             "The enemy hull has " + str(ehull) + " points left."] +
             [QPContent.__adv_station_state(STATIONS.get(id).name, state)
              for (id, state) in stations.iteritems()]
             + [QPContent.__report_end_game(end_game)] if s is not None]
              ))

    @staticmethod
    def __adv_station_state(station_name, station):
        if station.fire > 0:
            if station.damaged:
                return "Our " + station_name + " is damaged and on fire. "
            else:
                return "Our " + station_name + " is on fire. "
        if station.damaged:
            return "Our " + station_name + " is damaged."
        return None

    @staticmethod
    def __report_end_game(end_game):
        if end_game == END_GAME_STATES.PLAYER_HULL_DESTROYED:
            return "The hull has been destroyed, all is lost."
        if end_game == END_GAME_STATES.PLAYER_LIFE_SUPPORT_LOSS:
            return "Life support reserves is empty. " + \
                "The crew breaths its last breath " + \
                "as cold overtakes the ship."
        if end_game == END_GAME_STATES.OPPONENT_HULL_DESTROYED:
            return "The enemy ship bursts apart, the crew lets out a " + \
                "sigh of relief, then a cheer. On to the next challenge."
        return None
