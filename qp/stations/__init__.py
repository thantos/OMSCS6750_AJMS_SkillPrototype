"""Quick Particle Stations Module."""
from .auto_turret import AutoTurret
from .cockpit import Cockpit
from .life_support import LifeSupport
from .shields import Shields

__station_clases = [AutoTurret, Cockpit, LifeSupport, Shields]


"""Dictionary of station classes."""
STATIONS = {station.__name__: station() for station in __station_clases}

__all__ = ['AutoTurret', 'Cockpit', 'LifeSupport', 'Shields', 'STATIONS']
