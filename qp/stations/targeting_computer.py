"""Targeting Computer Station."""
from .base_station import BaseStation
from .. qp_constants import STATS


class TargetingComputer(BaseStation):
    """Targeting Computer Station.

    Working: Provides X to A.
    Manned: Provides additional A by X%.
    Damaged: Provides nothing.
    """

    BASE_VALUE = 1  # TODO
    BOOST_MOD = 1  # TODO

    def __init__(self):
        """Construct a Targeting Computer."""
        super(TargetingComputer, self). \
            __init__(
                "TARGETING_COMPUTER", "Targeting Computer", STATS.ACCURACY,
                self.BASE_VALUE, self.BOOST_MOD)
