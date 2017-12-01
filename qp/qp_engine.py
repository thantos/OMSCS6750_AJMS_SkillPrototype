"""Game Engine for Quick Particle."""
from state import QPGameState, StationState
from .qp_exceptions import CrewMemberInvalidException, \
    StationInvalidException, MemberAlreadyInStationException
from copy import deepcopy
from stations import STATIONS
from .qp_constants import STATS, STAT_CONSTANTS, END_GAME_STATES, BASE_STATS
import random


class QPEngine(object):
    """Quick Particle Game Engine.

    This class should be stateless.
    """

    def instruct_crew(self, game_state, member, station):
        """Validate a command to tell a crew member to move to a station.

        TODO make the crew and station selection more forgivingg

        game_state -- QPGameState, Current state of the crew
        member     -- String, Member name to move
        station    -- String, Station name
        """
        if type(game_state) is not QPGameState:
            raise ValueError("game_state must be a QPGameState Instance")

        if member not in game_state.ship.crew:
            raise CrewMemberInvalidException(member + " is not in the crew")

        if station not in game_state.ship.stations:
            raise StationInvalidException(station + " is not on the ship")

        if game_state.ship.crew[member].station == station:
            raise MemberAlreadyInStationException(
                member + " is already in " + station)

        state = deepcopy(game_state)

        state.ship.crew[member].station = station

        return state

    def advance(self, game_state):
        """Advance Time by one Turn.

        Report Current State
        Player Commands Crew.
        Update Stats based on new Position
        Combat
        Apply Tasks
        Repair/Fire Suppression
        Apply Combat Impacts
        Check for End Game States
        Repeat @ 1
        """
        if type(game_state) is not QPGameState:
            raise ValueError("game_state must be a QPGameState Instance")

        state = deepcopy(game_state)
        opponent = game_state.stage.opponent

        manned_stations = self.__get_manned_stations(state.ship.crew)

        # TODO collect stats based on stations

        station_stats = \
            self.__collect_stats_from_stations(
                state.ship.stations, manned_stations)

        # TODO reduce LS by LSD

        station_stats[STATS.LifeSupport] = \
            station_stats.get(STATS.LifeSupport, 0) \
            + STAT_CONSTANTS.LIFE_SUPPORT_DECAY

        # TODO update stats with the base stats and the station_stats

        current_stats = self.__update_stats(BASE_STATS, state.ship.stats)
        current_stats = self.__update_stats(current_stats, station_stats)

        # TODO combat

        (damage_player, damage_opponent) = \
            self.__combat(current_stats, opponent.stats)

        # TODO fire and damage to player station

        # TODO advance station states

        state.ship.stations = \
            self.__advance_stations_state(
                game_state.ship.stations, manned_stations)

        # TODO apply result of combat to stats

        station_stats[STATS.HULL_HEALTH] -= damage_player
        opponent.stats[STATS.HULL_HEALTH] -= damage_opponent

        # Store only the persistent stats. All opponent stats are persistent.
        state.ship.stats = self.__collect_persistent_stats(station_stats)

        # return

        return state

    def __get_manned_stations(self, crew):
        return set([
                    s.station for (c, s) in crew.iteritems()
                    if s.station is not None])

    def __collect_stats_from_stations(self, stations, manned_stations):
        # TODO Very gross... clean up
        maps = [
            STATIONS.get(station).handle(
                station in manned_stations and state.fire == 0)
            for (station, state) in stations.iteritems()
            if not state.damaged]

        stats = {}

        for m in maps:
            for (k, v) in m.iteritems():
                stats[k] = stats.get(k, 0) + v

        return stats

    def __update_stats(self, stats, station_stats):
        # TODO Handle max or ranges more gracefully
        cp = stats.copy()
        for (s, v) in station_stats.iteritems():
            c = cp.get(s, 0)
            if s == STATS.LIFE_SUPPORT:
                cp[s] = min(c + v, cp.get(STATS.MAX_LS, 0))
            elif s == STATS.HULL_HEALTH:
                cp[s] = min(c + v, cp.get(STATS.MAX_HULL_HEALTH, 0))
            else:
                cp[s] = c + v
        return cp

    def __combat(self, current_stats, opponent_stats):
        return (
            # Opponent attacks player, results in damage to player
            self.__attack(opponent_stats, current_stats),
            # Player attacks opponent, results in damage to opponet
            self.__attack(current_stats, opponent_stats))

    def __attack(self, attacker_stats, defender_stats):
        attacker_accuracy = attacker_stats.get(STATS.ACCURACY)
        attacker_power = attacker_stats.get(STATS.ATTACK_POWER)

        if attacker_accuracy > 0 and attacker_power > 0:
            defender_dodge = defender_stats.get(STATS.DODGE, 0)
            hit_chance = attacker_accuracy - defender_dodge
            if hit_chance > 0.0 and random.random() <= hit_chance:
                defender_shield = defender_stats.get(STATS.SHIELD, 0)
                damage = attacker_power - defender_shield
                return max(0, damage)
        return 0

    def __advance_stations_state(self, stations, manned_stations):
        return {
            station: self.__update_station(state, station in manned_stations)
            for (station, state) in stations.iteritems()}

    def __update_station(self, state, manned):
        fire = state.fire
        if manned:
            if fire > 0:  # remove fire
                return StationState(damaged=state.damaged)
            elif state.damaged:  # remove damage
                return StationState(damaged=False)
            return StationState()  # nothing, station is clean
        else:
            """
            if damaged stay damaged
            if clean, stay clean
            maintain current fire
            """
            if fire > 0:  # advance fire
                fire += 1
            # Damage if the fire is now stronger than the fire suppression
            damaged = state.damaged or fire > STAT_CONSTANTS.FIRE_SUPPRESSION
            return StationState(fire=fire, damaged=damaged)

    def __collect_persistent_stats(self, stats):
        """Collect persistent stats.

        These stats need to carry over during combat.
        They wil be set/reset at the beginning of a stage.
        They are not provided entirely by the stations like the others.
        This is not the most clear way to do this... but will work for now.
        TODO improve distiction between persistent and instant stats
        """
        return {
                s: v for (s, v) in stats.iteritems()
                if s in (STATS.HULL_HEALTH, STATS.LIFE_SUPPORT, STATS.WARP)}

    def check_for_endgame_states(self, game_state):
        """Evaluate the game state for end game scenerios."""
        if type(game_state) is not QPGameState:
            raise ValueError("game_state must be a QPGameState Instance")

        player_stats = game_state.ship.stats
        opponent_stats = game_state.stage.opponent.stats

        if player_stats.get(STATS.HULL_HEALTH) <= 0:
            return END_GAME_STATES.PLAYER_HULL_DESTROYED
        if player_stats.get(STATS.LIFE_SUPPORT) <= 0:
            return END_GAME_STATES.PLAYER_LIFE_SUPPORT_LOSS
        if opponent_stats.get(STATS.HULL_HEALTH) <= 0:
            return END_GAME_STATES.OPPONENT_HULL_DESTROYED
        return None
