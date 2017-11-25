"""Station Module."""


class Station(object):
    """Base station object."""

    def __init__(self, name):
        """Construct base station."""
        self.name = "name"

    def handle(self, boost):
        """Return stats to modify.

        Manned: Generally if the station is manned or not.
                May request boost for other reasons.
        """
        return {}
