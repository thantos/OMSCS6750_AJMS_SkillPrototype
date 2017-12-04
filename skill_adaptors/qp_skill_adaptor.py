"""QP Skill Adapator Module."""
from skill_helpers import build_response, \
    build_speechlet_response_enahnced, PlainResponse
from qp import QPRunner, CREW_MEMBERS, \
    CrewMemberInvalidException, StationInvalidException, QPContent, STATS, \
    BASE_STATS, CONSTANTS, STARTING_STATIONS, \
    MemberAlreadyInStationException, EndGameState
from qp.stations import STATIONS


class QPSkillAdaptor(object):
    """Translates skill logic into QP game logic."""

    def __init__(self):
        """Build QP Skill Adaptor."""
        self.__runner = QPRunner()

    def on_intent(self, intent_data, session):
        """Route intents within qp."""
        meta = session.get("meta", {}) if session is not None else {}
        game_state = meta.get("game_state", {})
        new_game_state = game_state
        response = build_speechlet_response_enahnced(
                QPContent.DEFAULT_RESPONSE,
                card=QPContent.DEFAULT_CARD, should_end_session=False)
        intent_name = intent_data.get("name")

        # New Game
        if game_state is None or game_state == {}:
            (response, new_game_state) = self.__handle_new_game()
        else:
            state = self.__runner.transform_game_state(game_state)
            slots = intent_data.get("slots")
            if intent_name == "instructCrewIntent":  # Instruct Crew
                (response, new_game_state) = \
                    self.__handle_instruct_crew(slots, state)
            if intent_name == "crewStateIntent":
                response = self.__handle_crew_state(slots, state)
            elif intent_name == "goIntent":  # Advance Combat
                (response, new_game_state) = \
                    self.__handle_combat(slots, state)

        # TODO this is gross, use immutable objects
        meta["game_state"] = self.__runner.to_json_friendly(new_game_state)
        session["meta"] = meta

        # TODO do more with game end
        # TODO keep session alive when not lost
        return build_response(session, response)

    def __handle_new_game(self):
        """Create a new game.

        NOTE: In the future, creating and priming a stage will be separate
        from creating a new ship.

        Create new ship
        Create the a new stage
        Prime the ship's stage persistent status.
        """
        game_state = self.__runner.new_game(
            CONSTANTS.STARTING_CREW_MEMBERS, STARTING_STATIONS)

        # Create a new stage/opponent
        new_stage = self.__runner.start_stage("Destroyer", {
            STATS.HULL_HEALTH: 50,
            STATS.ATTACK_POWER: 5,
            STATS.DODGE: 2,
            STATS.SHIELD: 0,
            STATS.ACCURACY: 4,
            STATS.MAX_HULL_HEALTH: 50
        })
        # Set the stage
        game_state.stage = new_stage

        # TODO Prime based on ship calculated ship stats,
        # for now MH and MLS canonot be upgraded
        game_state.ship.stats = \
            self.__runner.prime_ship_for_combat(BASE_STATS)

        # Welcome message, introduce the crew, introduce the stations
        crew = [
            CREW_MEMBERS.get(c).get("name")
            for c in game_state.ship.crew.keys()]

        stations = [
            STATIONS.get(s).name
            for s in game_state.ship.stations.keys()]

        text = QPContent.new_game_response(
            crew, stations, new_stage.opponent.name)

        response = build_speechlet_response_enahnced(text)

        return (response, game_state)

    def __handle_instruct_crew(self, slots, game_state):
        crew_id = self.__extract_id_from_slot(slots.get("crewSlot"))
        station_id = self.__extract_id_from_slot(slots.get("stationSlot"))

        try:
            (state, crew, station) = \
                self.__runner.instruct_crew(game_state, crew_id, station_id)

            response = build_speechlet_response_enahnced(
                QPContent.instruct_crew_response(crew["name"], station.name),
                reprompt=QPContent.INSTRUCT_CREW_REPROMPT,
                card=QPContent.INSTRUCT_CREW_CARD)
            return (response, state)
        except (CrewMemberInvalidException, StationInvalidException), e:
            response = build_speechlet_response_enahnced(
                PlainResponse(str(e)),
                QPContent.INSTRUCT_CREW_REPROMPT,
                card=QPContent.INVALID_INSTRUCTION_CARD)
            return (response, game_state)
        except MemberAlreadyInStationException, e:
            response = build_speechlet_response_enahnced(
                PlainResponse(str(e)),
                QPContent.INSTRUCT_CREW_REPROMPT,
                card=QPContent.INVALID_INSTRUCTION_CARD)
            return (response, game_state)

    def __handle_combat(self, slots, game_state):
        unassigned = [
            c for (c, s) in game_state.ship.crew.iteritems()
            if s.station is None]

        if len(unassigned) > 0:
            return (build_speechlet_response_enahnced(
                QPContent.unassigned_crew(
                    [CREW_MEMBERS[c]["name"] for c in unassigned],
                    [STATIONS[station].name
                     for station in game_state.ship.stations.keys()
                     if station not in game_state.ship.crew.values()]),
                    reprompt=PlainResponse("Move your crew to stations or " +
                    "say engage to continue.")),
                    game_state)

        (game_state, qp_results) = \
            self.__runner.advance_combat(game_state)

        is_end_game = len(filter(
            lambda r: issubclass(type(r), EndGameState), qp_results)) > 0

        return (build_speechlet_response_enahnced(
            QPContent.handle_qp_results_respone(qp_results),
            should_end_session=is_end_game,
            reprompt=PlainResponse("Move your crew to stations or " +
                "say engage to continue.")),
                game_state)

    def __handle_crew_state(self, slots, game_state):
        crew_id = self.__extract_id_from_slot(slots.get("crewSlot"))
        station_id = self.__extract_id_from_slot(slots.get("stationSlot"))

        response = None

        if station_id is not None:
            response = self.__get_station_state_response(
                station_id, game_state.ship)

        elif crew_id is not None:
            response = self.__get_crew_state_response(
                crew_id, game_state.ship.crew)

        # List all crew member's location
        if response is None:
            response = QPContent.cs_crew_stations_reponse(
                [(c, s.station)
                 for (c, s) in game_state.ship.crew.iteritems()])

        return build_speechlet_response_enahnced(
            response, card=QPContent.CREW_STATE_CARD)

    def __get_station_state_response(self, station_id, ship):
        if station_id in STATIONS:
            station_name = STATIONS.get(station_id).name
            if station_id in ship.stations:
                cs = [
                    c for (c, s) in ship.crew.iteritems()
                    if s.station == station_id]
                if len(cs) > 0:
                    # handle with the crew logic
                    return self.__get_crew_state_response(c[0], ship.crew)
                else:
                    return QPContent.cs_station_unmanned_response(
                            station_name)
            else:
                return QPContent.cs_station_not_avaliable_response(
                    station_name)
        else:
            return QPContent.cs_station_is_invalid_response(station_id)

    def __get_crew_state_response(self, crew_id, crew):
        if crew_id in CREW_MEMBERS:
            crew_name = CREW_MEMBERS[crew_id]["name"]
            if crew_id in crew:
                crew_state = crew[crew_id]
                if crew_state.station is not None:
                    return PlainResponse(
                        QPContent.cs_crew_crew_manning_station(
                            crew_name, STATIONS[crew_state.station].name))
                else:
                    return PlainResponse(
                        QPContent.cs_crew_not_assigned(crew_name))
            else:
                return QPContent.cs_crew_member_invalid_response(
                    crew_name)
        else:
            return QPContent.cs_crew_member_invalid_response(crew_id)

    # TODO make this more dynamic
    def __extract_id_from_slot(self, slot):
        try:
            return slot["resolutions"]["resolutionsPerAuthority"][0] \
                .get("values")[0]["value"]["id"]
        except Exception:
            return None
