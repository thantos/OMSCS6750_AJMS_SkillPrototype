"""Test the station module."""
from unittest import TestCase
from stations import Cockpit, AutoTurret, Shields, LifeSupport
from qp import STATS


class BaseStationTests(object):
    """Test all base stations."""

    def __init__(self, stat, base, boost, generator):
        """Construct Base Station Base Test Cases."""
        self.__stat = stat
        self.__base = base
        self.__boost = boost
        self.__gen = generator

    def setUp(self):
        """Setup."""
        self.undertest = self.__gen()

    def test_should_return_stat(self):
        """The station should boost the expected stat."""
        self.assertIn(self.__stat, self.undertest.handle(False))

    def test_should_return_base_value(self):
        """The station should boost the expected stat with the base value."""
        self.assertDictContainsSubset(
            {self.__stat: self.__base},
            self.undertest.handle(False))

    def test_should_return_non_0_base_value(self):
        """A unboosted station should return a value greater than 0."""
        self.assertGreater(self.undertest.handle(False)[self.__stat], 0)

    def test_should_return_boosted_value(self):
        """A boosted station should apply the boost value."""
        self.assertDictContainsSubset(
            {self.__stat: self.__base * self.__boost},
            self.undertest.handle(True))

    def test_should_return_non_0_boosted_value(self):
        """A unboosted station should return a value greater than 0."""
        self.assertGreater(self.undertest.handle(True)[self.__stat], 0)

    def test_boosted_is_greater_than_base(self):
        """A unboosted station should return a value greater than 0."""
        self.assertGreater(
            self.undertest.handle(True)[self.__stat],
            self.undertest.handle(False)[self.__stat])


class AutoTurretTests(BaseStationTests, TestCase):
    """Test AutoTurret."""

    def __init__(self, *args, **kwargs):
        """Pass in AutoTurret values."""
        super(AutoTurretTests, self).__init__(
            STATS.ATTACK_POWER, AutoTurret.BASE_VALUE, AutoTurret.BOOST_MOD,
            lambda: AutoTurret()
        )
        TestCase.__init__(self, *args, **kwargs)


class CockpitTests(BaseStationTests, TestCase):
    """Test Cockpit Station."""

    def __init__(self, *args, **kwargs):
        """Pass in Cockpit values."""
        super(CockpitTests, self).__init__(
            STATS.DODGE, Cockpit.BASE_VALUE, Cockpit.BOOST_MOD,
            lambda: Cockpit()
        )
        TestCase.__init__(self, *args, **kwargs)


class LifeSupportTests(BaseStationTests, TestCase):
    """Test Life Support Station."""

    def __init__(self, *args, **kwargs):
        """Pass in Cockpit values."""
        super(LifeSupportTests, self).__init__(
            STATS.LIFE_SUPPORT, LifeSupport.BASE_VALUE, LifeSupport.BOOST_MOD,
            lambda: LifeSupport()
        )
        TestCase.__init__(self, *args, **kwargs)


class ShieldsTests(BaseStationTests, TestCase):
    """Test Shields Station."""

    def __init__(self, *args, **kwargs):
        """Pass in Cockpit values."""
        super(ShieldsTests, self).__init__(
            STATS.SHIELD, Shields.BASE_VALUE, Shields.BOOST_MOD,
            lambda: Shields()
        )
        TestCase.__init__(self, *args, **kwargs)
