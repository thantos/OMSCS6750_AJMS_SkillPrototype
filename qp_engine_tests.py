from unittest import TestCase
from qp import QPEngine


class QPEngineTests(TestCase):
    def setUp(self):
        self.undertest = QPEngine()

    def test_(self):
        self.assertIsNotNone(self.undertest)

    def test_2(self):
        self.assertIsNotNone(self.undertest)
