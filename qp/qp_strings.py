"""QP Common Strings Module."""
from skill_helpers import PlainResponse, SSMLResponse, SimpleCard, \
    handle_text_list
from stations import STATIONS
from .qp_constants import CREW_MEMBERS
from .qp_combat_results import AttackMissed, AttackHit, StationStateActor, \
    StationDamageStateChange, StationFireStateChange, ResultThresholds, \
    HealthThresholdBreached, LifeSupportThresholdBreached, HullDestroyed, \
    LifeSupportDepleted


class QPContent(object):
    """Common Strings and Text output functions."""

    QUICK_PARTICLE_STRING = "Quick Particle"
    DEFAULT_OUTPUT = "Captain, I am not sure what you meant by that. " +\
        "Try asking the crew to move to stations " + \
        "or say engage to continue the battle."
    DEFAULT_RESPONSE = \
        PlainResponse(DEFAULT_OUTPUT)
    DEFAULT_CARD = SimpleCard(QUICK_PARTICLE_STRING, DEFAULT_OUTPUT)

    """
    New Game
    """

    NEW_GAME_INTRO = \
        "Captain, are you ok? Our core is damaged, our " + \
        "shields and warp drive are unusable. " + \
        "We should find another ship to scrap a core from, then we " + \
        "could get moving again."
    NEW_GAME_CARD_TITLE = "Quick Particle Ship Acquisition"
    STATION_DESCRIPTION = "You can assign crew members to our stations. " + \
        "Manned stations will operate more effectively. " + \
        "A crew member can also repair damaged stations or put out fires."
    MOVE_SUGGESTION_TEXT = \
        "You can assign your crew to stations by saying move " \
        + "crew name to station name. Say engage once you are ready " \
        + "to fight the enemy ship."

    @staticmethod
    def list_crew(crew_names):
        return "Our small crew is " + handle_text_list(crew_names) + "."

    @staticmethod
    def list_stations(station_names):
        return "Our functioning stations are " + \
            handle_text_list(station_names) + "."

    @staticmethod
    def describe_stage(opponent_name):
        # TODO Note, this is temporarily specific
        return "Luckily, There is an enemy ship called " + \
            opponent_name + \
            " off the port. It has begun firing on us."

    # TODO separate new game, stage, and instructions
    @staticmethod
    def new_game_response(crew_members, stations, opponent_name):
        return PlainResponse(
            " ".join([
             QPContent.NEW_GAME_INTRO,
             QPContent.describe_stage(opponent_name),
             "As a remminder, ",
             QPContent.list_crew(crew_members),
             QPContent.STATION_DESCRIPTION,
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

    """
    Advance
    """

    @staticmethod
    def unassigned_crew(unassigned_names, empty_stations):
        multiple_c = len(unassigned_names) > 1
        multiple_s = len(empty_stations) > 1
        return PlainResponse(
            handle_text_list(unassigned_names) +
            " " + ("have" if multiple_c else "has") +
            " not been assigned to a station." +
            " I suggest you assign them before we engage." +
            " You can say move crew member name to station name." +
            " The empty stations " + ("are" if multiple_s else "is") +
            " " + handle_text_list(empty_stations))

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

    """QP Results"""

    @staticmethod
    def handle_qp_results_respone(qp_results):
        return [resp for resp in
                [QPContent.handle_qp_result(r)
                 for r in qp_results] if resp is not None]

    @staticmethod
    def handle_qp_result(result):
        if isinstance(result, AttackMissed):
            return QPContent.__handle_attack_miss(result)
        elif isinstance(result, AttackHit):
            return QPContent.__handle_attack_hit(result)
        elif isinstance(result, StationDamageStateChange):
            return QPContent.__handle_station_damage_state_change(result)
        elif isinstance(result, StationFireStateChange):
            return QPContent.__handle_station_fire_state_change(result)
        elif isinstance(result, HealthThresholdBreached):
            return QPContent.__handle_health_threshold_breach(result)
        elif isinstance(result, LifeSupportThresholdBreached):
            return QPContent.__handle_life_support_threshold_breach(result)
        elif isinstance(result, LifeSupportDepleted):
            return QPContent.__handle_life_support_depleted(result)
        elif isinstance(result, HullDestroyed):
            return QPContent.__handle_hull_destroyed(result)

    @staticmethod
    def __handle_attack_miss(attack_miss):
        if attack_miss.player:
            return SSMLResponse(
                "<say-as interpret-as=\"interjection\">bah!</say-as> " +
                "we missed their ship.")
        else:
            return SSMLResponse(
                "<say-as interpret-as=\"interjection\">hooray</say-as> " +
                "they missed us.")

    @staticmethod
    def __handle_attack_hit(attack_hit):
        # TODO base result on damage done
        if attack_hit.player:
            return SSMLResponse(
                "<say-as interpret-as=\"interjection\">bam!</say-as> " +
                "we hit them!")
        else:
            return SSMLResponse(
                "<say-as interpret-as=\"interjection\">wham!</say-as> " +
                "they hit us captain.")

    @staticmethod
    def __handle_station_damage_state_change(station_damage):
        station_name = STATIONS.get(station_damage.station).name
        if station_damage.repaired_by is not None:
            crew_name = CREW_MEMBERS.get(station_damage.repaired_by)["name"]
            if station_damage.damaged_by is not None:
                return PlainResponse(
                    crew_name + " is repairing the " + station_name +
                    ", but it was futher damaged by enemy fire.")
            else:
                return PlainResponse(
                    crew_name + " has repaired the " + station_name)
        elif station_damage.damaged_by == StationStateActor.ATTACK:
            return PlainResponse(
                "The " + station_name + " has been damaged by enemy fire.")
        elif station_damage.damaged_by == StationStateActor.FIRE:
            return PlainResponse(
                "The fire in the " + station_name + " has damaged it.")

    @staticmethod
    def __handle_station_fire_state_change(station_fire):
        station_name = STATIONS.get(station_fire.station).name
        if station_fire.extinguished_by is not None:
            crew_name = CREW_MEMBERS.get(station_fire.extinguished_by)["name"]
            if station_fire.start_by is not None:
                return PlainResponse(
                    "Enemy fire expanded the fire " + crew_name +
                    " put out in the " + station_name)
            else:
                return PlainResponse(
                    crew_name + " has extinguished the fire in the " +
                    station_name)
        elif station_fire.start_by == StationStateActor.ATTACK:
            return PlainResponse(
                "The " + station_name + " has started on fire.")

    @staticmethod
    def __handle_health_threshold_breach(health_breach):
        if not health_breach.up:
            if health_breach.player:
                if health_breach.threshold == ResultThresholds["HIGH"]:
                    return PlainResponse("The hull is holding, captain.")
                elif health_breach.threshold == ResultThresholds["MID"]:
                    return PlainResponse("The hull is weakening, captain.")
            elif health_breach.threshold == ResultThresholds["LOW"]:
                    return PlainResponse(
                        "The hull is critically damaged, captain.")
            else:
                if health_breach.threshold == ResultThresholds["HIGH"]:
                    return PlainResponse(
                        "The enemy hull is withstnding our impacts, captain.")
                elif health_breach.threshold == ResultThresholds["MID"]:
                    return PlainResponse(
                        "The enemy hull is showing weakness, captain.")
                elif health_breach.threshold == ResultThresholds["LOW"]:
                    return PlainResponse(
                        "The enemy is critically damaged, let's finish them!")
        else:
            pass  # TODO handle up phrases

    @staticmethod
    def __handle_life_support_threshold_breach(ls_breach):
        if not ls_breach.up:
            if ls_breach.threshold == "HIGH":
                return PlainResponse("We are losing life support charge!")
            elif ls_breach.threshold == "MID":
                return PlainResponse(
                    "Life Support state continues to worsen, " +
                    "consider repairing the Life Support station.")
            elif ls_breach.threshold == "LOW":
                return PlainResponse(
                    "Life support is critical, " +
                    "repair or we will die, captain!")
        else:
            if ls_breach.threshold == "FULL":
                return PlainResponse("Life support is full restored.")
            elif ls_breach.threshold == "HIGH":
                return PlainResponse("Life Support is improving.")
            elif ls_breach.threshold == "MID":
                return PlainResponse(
                    "Life Support out of a critical state.")

    @staticmethod
    def __handle_hull_destroyed(hull_destroyed):
        if hull_destroyed.player:
            return PlainResponse("The hull has been destroyed, all is lost.")
        else:
            return PlainResponse(
                "The enemy ship bursts apart, the crew lets out a " +
                "sigh of relief, then a cheer. On to the next challenge.")

    @staticmethod
    def __handle_life_support_depleted(life_support_depleted):
        return PlainResponse(
                "Life support reserves is empty. " +
                "The crew breaths its last breath " +
                "as cold overtakes the ship.")
