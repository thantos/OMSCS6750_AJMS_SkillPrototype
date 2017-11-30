"""Base Station."""
from .station import Station


class BaseStation(Station):
    """Base Station.

    Returns a single stat with some base value and
    can be boosted by some percent.
    """

    def __init__(self, id, name, stat, base, boost):
        """Construct a basic station that changes a single station."""
        super(BaseStation, self).__init__(id, name)
        self.__stat = stat
        self.__base = base
        self.__boost = boost

    def handle(self, boost):
        """Provide __stat."""
        return {
            self.__stat: self.__base * (1 + (self.__boost if boost else 0))
        }
