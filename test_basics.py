from unittest import TestCase
from lambda_function import *
import json


class Test_Basics(TestCase):
    def setUp(self):
        self.scene_name = 'tutorial'
        self.json = json.load(open('scenes/tutorial.json'))

    def test_one_round(self):
        response = loadScene(self.scene_name, {}, {})
        first_round = response['response']['outputSpeech']['text']

        expected_first_round = self.json['rounds'][0]
        self.assertEqual(first_round, expected_first_round)


