""""""
from .qp_constants import STATS
from .qp_combat_results import AttackHit, AttackMissed, \
    StationDamageStateChange, StationFireStateChange, StationStateActor, \
    ResultThresholds, HealthThresholdBreached, LifeSupportThresholdBreached, \
    HullDestroyed, LifeSupportDepleted


class QPResultEngine(object):
    """Process inputs into result state objects.

    Helps determine details on what happens during a round.
    """

    """Combat Results"""

    def record_combat_result(self, player_damage, opponent_damage):
        """Compute result objects directly out of combat."""
        player_attack = QPResultEngine.__attack_state(opponent_damage)
        opponent_attack = QPResultEngine.__attack_state(player_damage, False)
        return [player_attack, opponent_attack]

    @staticmethod
    def __attack_state(damage, player=True):
        """Record the attack state.

        TODO Assumes that 0 damage is a miss, could be blocked.
        """
        return AttackHit(player, damage) \
            if(damage > 0) else AttackMissed(player)

    """Station State Change"""

    def record_station_advance_result(self, start_stations,
                                      advance_stations, final_stations, crew):
        """Record result objects for chaning of station state.

        TODO remove assumption that a and b are the same.
        """
        results = []
        for (id, start_state) in start_stations.iteritems():
            results += QPResultEngine.__station_stats(
                id, start_state, advance_stations.get(id),
                final_stations.get(id), crew)
        return results

    @staticmethod
    def __station_stats(id, start_state, advance_state, final_state, crew):
        cm = QPResultEngine.__find_crew_in_station(id, crew)
        results = []
        if QPResultEngine.__fire_state_change(start_state,
                                              advance_state,
                                              final_state):
            # Fire is started if the state changed and fire is non 0
            started_by = StationStateActor.ATTACK \
                if final_state.fire > 0 else None
            # Fire was extinguished if the state changed
            # and fire is 0 before combat
            # Note: fire may be both exstinguished and started the same round
            extinguished_by = cm \
                if start_state.fire > 0 and advance_state.fire == 0 else None
            results += [StationFireStateChange(
                id, start_by=started_by, extinguished_by=extinguished_by)]
        if QPResultEngine.__damaged_state_change(start_state,
                                                 advance_state,
                                                 final_state):
            damaged_by = QPResultEngine.__station_damaged_by(start_state,
                                                             advance_state,
                                                             final_state)
            repaired_by = cm if start_state.damaged and \
                not advance_state.damaged else None
            results += [StationDamageStateChange(
                id, damaged_by=damaged_by, repaired_by=repaired_by)]
        return results

    @staticmethod
    def __fire_state_change(start, adv, final):
        """Define fire change as 0 to non 0 or vise versa."""
        return ((start.fire > 0) != (adv.fire > 0)) or ((adv.fire > 0) != (final.fire > 0))

    @staticmethod
    def __damaged_state_change(start, adv, final):
        """Define damaged change as damaged to not damaged changed at step."""
        return start.damaged != adv.damaged or adv.damaged != final.damaged

    @staticmethod
    def __station_damaged_by(start, adv, final):
        if start.fire > 0 and adv.damaged and start.damaged != adv.damaged:
            return StationStateActor.FIRE
        if adv.damaged != final.damaged:
            return StationStateActor.ATTACK

    @staticmethod
    def __find_crew_in_station(station_id, crew_members):
        r = [c for (c, s) in crew_members.iteritems() if s.station == station_id]
        if len(r) > 0:
            return r[0]
        return None

    """Thresholds"""

    def record_stat_threshold(self, start_stats_player, end_stats_player,
                              start_stats_opponent, end_stats_opponent):
        (health_direction, health_threshold) = \
            QPResultEngine.__calculate_threshold(
                start_stats_player.get(STATS.HULL_HEALTH),
                end_stats_player.get(STATS.HULL_HEALTH),
                end_stats_player.get(STATS.MAX_HULL_HEALTH),
                ResultThresholds)
        (ls_direction, ls_threshold) = \
            QPResultEngine.__calculate_threshold(
                start_stats_player.get(STATS.LIFE_SUPPORT),
                end_stats_player.get(STATS.LIFE_SUPPORT),
                end_stats_player.get(STATS.MAX_LS),
                ResultThresholds)
        (health_direction_opp, health_threshold_opp) = \
            QPResultEngine.__calculate_threshold(
                start_stats_opponent.get(STATS.HULL_HEALTH),
                end_stats_opponent.get(STATS.HULL_HEALTH),
                end_stats_opponent.get(STATS.MAX_HULL_HEALTH),
                ResultThresholds)
        results = []
        if health_threshold is not None:
            results += \
                [HealthThresholdBreached(health_direction, health_threshold)]
        if health_threshold_opp is not None:
            results += \
                [HealthThresholdBreached(
                    health_direction_opp, health_threshold_opp, False)]
        if ls_threshold is not None:
            results += \
                [LifeSupportThresholdBreached(ls_direction, ls_threshold)]
        return results

    @staticmethod
    def __calculate_threshold(start, end, max, thresholds):
        """

        example:
        max = 100
        start = 80
        end = 70
        down thresholds[75, 50, 30]
        were above 75, now below 75 == down and 70
        max = 100
        start = 45
        end = 55
        up thresholds[100, 50]
        were below 45, now above 50 == up and 50
        """
        if start == end:
            return (None, None)
        up = start < end
        s_p = (start * 100) / max
        e_p = (end * 100) / max

        new_threshold = None
        s_threshold = QPResultEngine.__find_nearest_key(s_p, thresholds, up)
        e_threshold = QPResultEngine.__find_nearest_key(e_p, thresholds, up)
        if s_threshold != e_threshold:
            new_threshold = e_threshold
        return (up, new_threshold)

    @staticmethod
    def __find_nearest_key(percent, threshold_map, up=False):
        for (k, v) in sorted(threshold_map.iteritems(),
                             key=lambda x: x[1], reverse=up):
            if (up and v <= percent) or (not up and v >= percent):
                return k
        return None

    """ End Game """

    def record_end_game(self, player_stats, opponent_stats):
        record = []
        if player_stats.get(STATS.HULL_HEALTH) <= 0:
            record += [HullDestroyed(player=True)]
        if player_stats.get(STATS.LIFE_SUPPORT) <= 0:
            record += [LifeSupportDepleted()]
        if opponent_stats.get(STATS.HULL_HEALTH) <= 0:
            record += [HullDestroyed(player=False)]
        return record
