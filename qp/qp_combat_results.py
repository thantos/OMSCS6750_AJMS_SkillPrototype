class QPResult(object):
    pass


""" Hit/Damage """


class AttackMissed(QPResult):
    """Attack missed, which means the attack was dodged.

    TODO Expand to reflet to crew member who caused this.
    """
    def __init__(self, player=True):
        self.player = player


class AttackHit(QPResult):
    """Attack hit, dodge failed."""
    def __init__(self, player=True, damage=0):
        self.player = player
        self.damage = damage

# TODO Add AttackBlocked for shielded attacks


""" Repair """


class StationStateActor(object):
    ATTACK = "Attack"
    FIRE = "FIRE"


# Repair but...
class StationDamageStateChange(QPResult):

    def __init__(self, station, damaged_by=None, repaired_by=None):
        self.station = station
        self.damaged_by = damaged_by
        self.repaired_by = repaired_by


class StationFireStateChange(QPResult):

    def __init__(self, station, start_by=None, extinguished_by=None):
        self.station = station
        self.extinguished_by = extinguished_by
        self.start_by = start_by


""" Thresholds """


"""Key to percent threshold"""
ResultThresholds = {
    "FULL": 100,
    "HIGH": 75,
    "MID": 50,
    "LOW": 30}


# Health threshold change
class HealthThresholdBreached(QPResult):

    def __init__(self, up=False, threshold=None, player=True):
        self.up = up
        self.threshold = threshold
        self.player = player


# Life Support threshold change
class LifeSupportThresholdBreached(QPResult):

    def __init__(self, up=False, threshold=None):
        self.up = up
        self.threshold = threshold
