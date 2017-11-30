"""QP Common Strings Module."""
from skill_helpers import PlainResponse, SSMLResponse, SimpleCard


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
    def new_game_response(crew_members, stations):
        return PlainResponse(
            " ".join([
             QPContent.NEW_GAME_INTRO,
             QPContent.list_crew(crew_members),
             QPContent.list_stations(stations),
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
